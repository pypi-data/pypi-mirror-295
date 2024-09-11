import warnings
import logging
import torch
from peft import AutoPeftModelForCausalLM
import bitsandbytes as bnb
from transformers import AutoTokenizer, BitsAndBytesConfig


# Suppress all warnings
warnings.filterwarnings("ignore")
# Suppress all the unnecessary info/warning logs
logging.getLogger("transformers").setLevel(logging.ERROR)


def load_finetuned_model(
    base_model_path: str,
    checkpoint_path: str,
    optimize: str = '4-bit',    
    device: str = "auto",
    use_flash_attn: bool = False
):
    """
    Load the tokenizer and fine-tuned LLM model with optional 4-bit quantization.

    Args:
        base_model_path (str): The directory path to the base model.
        checkpoint_path (str): The directory path to the fine-tuned model checkpoint.
        optimize (str): The optimization level for the model. Options are '4-bit', '8-bit', '16-bit', or None. Defaults to '4-bit'.
        device (str): The device to load the model onto. Defaults to 'auto'.
        use_flash_attn (bool, optional): Run the flash-attention implementation. Defaults to False.

    Returns:
        tuple: A tuple containing the loaded tokenizer and model.
    """
    
    # Load the tokenizer with specified padding side and fast mode
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_path, 
        padding_side='left', 
        use_fast=True
    )

    # Define quantization configurations for 4-bit and 8-bit
    quantization_configs = {
        '4-bit': BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",  # "fp4" is also an option
            bnb_4bit_compute_dtype=torch.bfloat16  # Can be torch.float16 or torch.bfloat16
        ),
        '8-bit': BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_use_double_quant=True,
            bnb_8bit_quant_type="dynamic",  # "static" is also an option
            bnb_8bit_compute_dtype=torch.bfloat16  # Can be torch.float16 or torch.bfloat16
        ),
    }

    model_kwargs = {
        "device_map" : device,
        "return_dict" : True
    }
    if use_flash_attn==True:
        model_kwargs["attn_implementation"] = "flash_attention_2"

    # Load the model based on the selected optimization level
    if optimize in quantization_configs:
        model = AutoPeftModelForCausalLM.from_pretrained(
            checkpoint_path,
            quantization_config=quantization_configs[optimize],
            # low_cpu_mem_usage=True,
            torch_dtype=torch.float16,
            **model_kwargs
        )
    elif optimize == '16-bit':
        model = AutoPeftModelForCausalLM.from_pretrained(
            checkpoint_path,
            torch_dtype=torch.float16,  # Using half precision (16-bit)
            **model_kwargs
            # low_cpu_mem_usage=True,
        )
    elif optimize is None:
        model = AutoPeftModelForCausalLM.from_pretrained(
            checkpoint_path,
            **model_kwargs
            # low_cpu_mem_usage=True,
        )
    else:
        raise ValueError(f"Invalid optimization level: {optimize}. Choose from '4-bit', '8-bit', '16-bit', or None.")

    return model, tokenizer