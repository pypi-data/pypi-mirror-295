__version__ = "0.1.3"

__author__ = "Nilavo Boral"


from .download import download_hf_model
from .inference import load_model, get_response, prepare_pipeline, chat
from .finetune import find_linear_layers, finetune_llm
from .load_finetuned_llm import load_finetuned_model
from .data_prep import llm_data_process
    

__all__ = [
    "download_hf_model",
    "load_model", "get_response", 
    "prepare_pipeline", "chat",
    "find_linear_layers", "finetune_llm",
    "load_finetuned_model",
    "llm_data_process"
]

__doc__ = {
    "download_hf_model": 
    """
    Downloads a model from Hugging Face to a specified local directory.

    Args:
        model_id (str): The name of the model to download from Hugging Face.
        local_dir (str): The local directory where the model should be saved.
        hf_token: (str): Your HuggingFace access token for login.
                            If you have already logged in previously, this is not required.
                            You can find your access token by visiting the following link:
                            https://huggingface.co/settings/tokens .
                            Default is None.
        
    Raises:
        subprocess.CalledProcessError: If the download command fails.
    """,

    "load_model": 
    """
    Loads a model from local folder with optional quantization and optimization.

    Args:
        model_path (str): The identifier of the model to load.
        optimize (str): The optimization level for the model. Options are '4-bit', '8-bit', '16-bit', or None. Defaults to '4-bit'.
        device (str): The device to load the model onto. Options are 'auto', 'cuda', or 'cpu'. Defaults to 'auto'.
        use_flash_attn (bool, optional): Run the flash-attention implementation. Defaults to False.

    Returns:
        model: The loaded model.
        tokenizer: The tokenizer associated with the model.

    Raises:
        ValueError: If an invalid optimization level is provided.
    """,

    "get_response": 
    """
    Generates a response from a language model based on a given prompt, with optional individual generation arguments.

    Args:
        model: The pre-loaded model to use for text generation.
        tokenizer: The tokenizer associated with the model.
        prompt (str): The input string to generate a response for.
        max_new_tokens (int, optional): Maximum number of new tokens to generate. Default is 500.
        temperature (float, optional): Sampling temperature. Higher values make the output more random. Range: 0.0 to 2.0. Default is 1.0.
        top_p (float, optional): Top-p sampling. Keeps the cumulative probability of top tokens below this threshold. Range: 0.0 to 1.0. Default is 1.0.
        repetition_penalty (float, optional): Penalty for repeated phrases or tokens. Range: 1.0 to 2.0. Default is 1.0.

    Returns:
        str: The generated response from the model.

    Raises:
        ValueError: If the output format from the model is not as expected.
    """,

    "prepare_pipeline": 
    """
    Prepares the text generation pipeline with the model, tokenizer, and optional generation arguments.

    Args:
        model: The pre-loaded model to use for text generation.
        tokenizer: The tokenizer associated with the model.
        max_new_tokens (int, optional): Maximum number of new tokens to generate. Default is 500.
        temperature (float, optional): Sampling temperature. Higher values make the output more random. Range: 0.0 to 2.0. Default is 1.0.
        top_p (float, optional): Top-p sampling. Keeps the cumulative probability of top tokens below this threshold. Range: 0.0 to 1.0. Default is 1.0.
        repetition_penalty (float, optional): Penalty for repeated phrases or tokens. Range: 1 to 2. Range: 1.0 to 2.0. Default is 1.0.

    Returns:
        Tuple containing the pipeline object and the generation arguments.
    """,


    "chat": 
    """
    Generates a response based on the prompt and optional messages, using the provided text generation pipeline.

    Args:
        text_gen_pipe: The text generation pipeline initialized using `prepare_pipeline`.
        generation_args (dict): Arguments that define how the text generation will be performed.
        prompt (str): The input prompt to generate a response for.
        messages (list, optional): List of message dictionaries containing roles and content.
                                    If you want to start a fresh chat, simply don't pass the messages argument.

    Returns:
        The updated messages list where the generated text is appended to the last message.

    Raises:
        ValueError: If the output format from the model is not as expected.
    """,


    "find_linear_layers": 
    """
    Identify all linear 4-bit modules in the given model, to set the target modules during fine-tuning.

    Args:
        model (torch.nn.Module): The model in which the linear 4-bit modules are to be found.

    Returns:
        list: A sorted list of unique module names that correspond to the 4-bit linear layers 
        within the model. The 'lm_head' module is excluded.
    """,


    "finetune_llm": 
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
        wandb_key (str): Your own wandb login key.
                            You can find your wandb key by going to this link: https://wandb.ai/authorize .

    Returns:
        Tuple[PreTrainedModel, Trainer, List[dict]]: The fine-tuned model, trainer instance, and training logs.
    """,


    "load_finetuned_model": 
    """
    Load the tokenizer and fine-tuned LLM model with optional 4-bit quantization.

    Args:
        base_model_path (str): The directory path to the base model.
        checkpoint_path (str): The directory path to the fine-tuned model checkpoint.
        optimize (str): The optimization level for the model. Options are '4-bit', '8-bit', '16-bit', or None. Defaults to '4-bit'.
        device (str): The device to load the model onto. Defaults to 'auto'.

    Returns:
        tuple: A tuple containing the loaded tokenizer and model.
    """,


    "llm_data_process": 
    """
    Prepare data for LLM fine-tuning by creating input-output pairs using a chat template.
    
    Args:
        tokenizer (PreTrainedTokenizer): Tokenizer for processing text.
        df (pd.DataFrame): Input data containing user queries and assistant responses.
        df_category (str): {'qa', 'not-qa'} 
            Indicates whether the task is question-answering ('qa') or another type of task ('not-qa').
        feature_cols (list): List of column names containing the model's input.
        target_cols (list): List of column names containing the assistant's responses.
        user_prompt (str): Template to structure user queries.

    Returns:
        pd.DataFrame: A DataFrame with formatted text for fine-tuning.
    """
}