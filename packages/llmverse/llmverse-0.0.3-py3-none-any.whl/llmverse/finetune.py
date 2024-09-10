import warnings
import pandas as pd
from typing import Tuple, List, Union
import wandb
import bitsandbytes as bnb
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model, AutoPeftModelForCausalLM
from datasets import Dataset
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling


# Suppress all warnings
warnings.filterwarnings("ignore")


def find_linear_layers(model):
    """
    Identify all linear 4-bit modules in the given model, to set the target modules during fine-tuning.

    Args:
        model (torch.nn.Module): The model in which the linear 4-bit modules are to be found.

    Returns:
        list: A sorted list of unique module names that correspond to the 4-bit linear layers 
        within the model. The 'lm_head' module is excluded.
    """
    linear_modules = {}

    for name, module in model.named_modules():
        if isinstance(module, bnb.nn.Linear4bit):
            # Handle both nested and top-level module names
            names = name.split(".")
            key = names[-2] if len(names) > 1 else "top module"
            linear_modules.setdefault(key, set()).add(names[-1])

    return linear_modules




def finetune_llm(
    model,
    tokenizer,
    target_modules: List[str],
    lora_rank: int,
    df: pd.DataFrame,
    validation_percent: float,
    max_steps: int,
    epochs: int,
    learning_rate: float,
    output_dir_name: str = "outputs",
    use_wandb: bool = False,
    wandb_key: str = None
):
    """
    Fine-tune a language model using LoRA (Low-Rank Adaptation) for efficient training.
    The training dataset is split into training and validation sets.

    Args:
        model (PreTrainedModel): The pre-trained model to be fine-tuned.
        tokenizer (PreTrainedTokenizer): Tokenizer to process input data.
        target_modules (List[str]): List of module names to be adapted with LoRA.
        lora_rank (int): LoRA rank (size of low-rank matrices).
        df (pd.DataFrame): The dataset containing input-output pairs for fine-tuning.
        validation_percent (float): Percentage of data used for validation.
        max_steps (int): Maximum number of training steps.
        epochs (int): Number of training epochs.
        learning_rate (float): Learning rate for the optimizer.
        output_dir_name (str, optional): Directory name to save the model outputs. Defaults to "outputs".
        use_wandb (bool, optional): Whether to use wandb for logging. Defaults to False.
        wandb_key (str): Your wandb access key for login.
                            If you have already logged in previously, this is not required.
                            You can find your wandb key by going to this link: https://wandb.ai/authorize .

    Returns:
        Tuple[PreTrainedModel, Trainer, List[dict]]: The fine-tuned model, trainer instance, and training logs.
    """
    # Training arguments
    training_args = {
            "per_device_train_batch_size" : 1,
            "per_device_eval_batch_size" : 2,
            "gradient_accumulation_steps" : 4,
            "warmup_steps" : 2,
            "max_steps" : max_steps,
            "num_train_epochs" : epochs,  # Increase number of epochs
            "evaluation_strategy" : "steps",
            "learning_rate" : learning_rate,
            "report_to" : "none",
            "eval_steps" : 1,  # More frequent validation loss logging
            "logging_steps" : 1, # More frequent training loss logging
            "load_best_model_at_end" : True,  # Load the best model at the end of training
            "output_dir" : output_dir_name,
            "optim" : "paged_adamw_8bit",
    }
    if use_wandb==True:
        if wandb_key is not None:
            try:
                wandb.login("allow", wandb_key)
                training_args['report_to'] = "wandb"
            except Exception as e:
                print(f"Error logging in to wandb: {e}")
                raise
                return
        else:
            print("\nUse your own wandb token for login.\nYou can find your access token by going to this link: https://wandb.ai/authorize \n")
            return

    # Enable gradient checkpointing for memory efficiency
    model.gradient_checkpointing_enable()
    # Prepare the model for k-bit training
    model = prepare_model_for_kbit_training(model)

    # Set up LoRA configuration
    config = LoraConfig(
        r=lora_rank,
        lora_alpha=32,
        target_modules=target_modules,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    # config.inference_mode = False ### ADDED
    model = get_peft_model(model, config)

    # Split the dataset into training and validation sets
    data_size = len(df)
    n = round(data_size*(1-validation_percent/100))
    # st.success(f'split {n}')

    train_df = df[:n]
    val_df = df[n:]

    train_data = Dataset.from_pandas(train_df)
    train_data = train_data.map(lambda samples: tokenizer(samples["text"]), batched=True)

    val_data = Dataset.from_pandas(val_df)
    val_data = val_data.map(lambda samples: tokenizer(samples["text"]), batched=True)

    # Define a training strategy with frequent evaluation and logging
    tokenizer.pad_token = tokenizer.eos_token # </s> # needed for tokenizer
    trainer = Trainer(
        model=model,
        train_dataset=train_data,
        eval_dataset=val_data,
        args=TrainingArguments(**training_args),
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    # Disable cache during training to avoid warnings
    model.config.use_cache = False  # silence the warnings. Please re-enable for inference!
    trainer.train()

    logs = trainer.state.log_history

    return model, trainer, logs