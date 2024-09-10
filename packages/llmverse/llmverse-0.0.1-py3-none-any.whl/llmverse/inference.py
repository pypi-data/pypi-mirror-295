import warnings
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import bitsandbytes as bnb
import torch
from typing import Optional, List, Dict, Tuple


# Suppress all warnings
warnings.filterwarnings("ignore")
# Suppress all the unnecessary info/warning logs
logging.getLogger("transformers").setLevel(logging.ERROR)


def load_model(
    model_path: str, 
    optimize: str = '4-bit', 
    device: str = 'auto', 
    use_flash_attn: bool = False
):
    """
    Loads a model from local folder with optional quantization and optimization.

    Args:
        model_path (str): The identifier of the model to load.
        optimize (str): The optimization level for the model. Options are '4-bit', '8-bit', '16-bit', or None. Defaults to '4-bit'.
        device (str): The device to load the model onto. Defaults to 'auto'.
        use_flash_attn (bool, optional): Run the flash-attention implementation. Defaults to False.

    Returns:
        model: The loaded model.
        tokenizer: The tokenizer associated with the model.

    Raises:
        ValueError: If an invalid optimization level is provided.
    """
    # Load the tokenizer with left padding and fast mode
    tokenizer = AutoTokenizer.from_pretrained(
        model_path, 
        padding_side='left', 
        use_fast=True
    )
    
    # Define a mapping for quantization configurations
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
        "trust_remote_code" : True
    }
    if use_flash_attn==True:
        model_kwargs["attn_implementation"] = "flash_attention_2"

    # Load the model based on the optimization level
    if optimize in quantization_configs:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=quantization_configs[optimize],
            **model_kwargs
        )
    elif optimize == '16-bit':
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,  # Using half precision (16-bit)
            **model_kwargs
        )
    elif optimize is None:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            **model_kwargs
        )
    else:
        raise ValueError(f"Invalid optimization level: {optimize}. Choose from '4-bit', '8-bit', '16-bit', or None.")
    
    return model, tokenizer



def prepare_pipeline(
    model,
    tokenizer,
    max_new_tokens: Optional[int] = 500,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    repetition_penalty: Optional[float] = None
):
    """
    Prepares the text generation pipeline with the model, tokenizer, and optional generation arguments.

    Args:
        model: The pre-loaded model to use for text generation.
        tokenizer: The tokenizer associated with the model.
        max_new_tokens (int, optional): Maximum number of new tokens to generate. Default is 500.
        temperature (float, optional): Sampling temperature. Higher values make the output more random. Range: 0.0 to 2.0. Default is 1.0.
        top_p (float, optional): Top-p sampling. Keeps the cumulative probability of top tokens below this threshold. Range: 0.0 to 1.0. Default is 1.0.
        repetition_penalty (float, optional): Penalty for repeated phrases or tokens. Range: 1.0 to 2.0. Default is 1.0.

    Returns:
        Tuple containing the pipeline object and the generation arguments.
    """
    # Initialize the text-generation pipeline
    text_gen_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )

    # Prepare generation arguments
    generation_args = {
        "max_new_tokens" : max_new_tokens,
        "return_full_text" : False,
        "do_sample" : False
    }
    if temperature is not None:
        generation_args["temperature"] = temperature
    if top_p is not None:
        generation_args["top_p"] = top_p
    if repetition_penalty is not None:
        generation_args["repetition_penalty"] = repetition_penalty

    return text_gen_pipe, generation_args



def get_response(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: Optional[int] = 500,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    repetition_penalty: Optional[float] = None
) -> str:
    """
    Generates a response from a language model based on a given prompt, with optional individual generation arguments.

    Args:
        model: The pre-loaded model to use for text generation.
        tokenizer: The tokenizer associated with the model.
        prompt (str): The input prompt to generate a response for.
        max_new_tokens (int, optional): Maximum number of new tokens to generate. Default is 500.
        temperature (float, optional): Sampling temperature. Higher values make the output more random. Range: 0.0 to 2.0. Default is 1.0.
        top_p (float, optional): Top-p sampling. Keeps the cumulative probability of top tokens below this threshold. Range: 0.0 to 1.0. Default is 1.0.
        repetition_penalty (float, optional): Penalty for repeated phrases or tokens. Range: 1.0 to 2.0. Default is 1.0.

    Returns:
        str: The generated response from the model.

    Raises:
        ValueError: If the output format from the model is not as expected.
    """
    # Prepare the pipeline and generation arguments
    text_gen_pipe, generation_args = prepare_pipeline(
        model,
        tokenizer,
        max_new_tokens,
        temperature,
        top_p,
        repetition_penalty
    )

    # Create the input message for the model
    messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]

    # Generate the output
    try:
        if generation_args:
            output = text_gen_pipe(messages, **generation_args)
        else:
            output = text_gen_pipe(messages)
    except Exception as e:
        raise RuntimeError(f"Failed to generate response: {str(e)}")

    # Extract the response text from the output
    try:
        response = output[0]['generated_text']
    except (KeyError, IndexError) as e:
        raise ValueError("Unexpected output format from the model: {}".format(e))

    return response



def chat(
    text_gen_pipe,
    generation_args: Dict,
    prompt: str,
    messages: Optional[List[Dict[str, str]]] = None
) -> List[Dict[str, str]]:
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
    """
    # Initialize messages if not provided and append the user prompt
    if messages is None:
        messages = [{"role": "user", "content": prompt}]
    else:
        messages.append({"role": "user", "content": prompt})

    # Perform text generation
    try:
        if generation_args:
            output = text_gen_pipe(messages, **generation_args)
        else:
            output = text_gen_pipe(messages)
    except Exception as e:
        raise RuntimeError(f"Failed to generate response: {str(e)}")

    # Extract the generated response text
    try:
        response = output[0]['generated_text']
        messages.append({"role": "assistant", "content": response})
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected output format from the model: {str(e)}")

    return messages
