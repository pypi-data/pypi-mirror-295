# llmverse (Discover the Universe of LLMs)

The llmverse is your comprehensive toolkit for all things LLM (Large Language Model). From downloading and quantizing to generating responses and fine-tuning, it handles every aspect of working with large language models in one unified package.

Developed by Nilavo Boral, 2024. [LinkedIn](https://www.linkedin.com/in/nilavo-boral-123bb5228/)


# Test notebooks

- Run any LLM: [Colab notebook](https://colab.research.google.com/drive/1ToeI4I7s03_NV94ZxNymQRmUkrDtVkGR#scrollTo=jeOPDVvblNLK)

- Chat with any LLM: [Colab notebook](https://colab.research.google.com/drive/12WNTMyhtDEfYKrJkl_b7N3tnLgoirjRp#scrollTo=jeOPDVvblNLK)

- Fine-tune any LLM: [Colab notebook](https://colab.research.google.com/drive/1M6PEksDGIpUhNAYRhNpCo_vs38332v3O#scrollTo=jeOPDVvblNLK)

- Run fine-tuned LLM: [Colab notebook](https://colab.research.google.com/drive/1-FhXLL8j6F8bHng52m1yl9FdHvOaYDns#scrollTo=jeOPDVvblNLK)


# Installation Guide

- ### Prerequisite:

Ensure you have **CUDA version 11.6 or higher** installed. You can check your CUDA version using the following command:

```bash
nvcc --version
```


- ### To install llmverse, use the following command:
```python
pip install llmverse

```
If you encounter any installation issues, try installing the **packaging**, **wheel**, and **torch** packages separately, and then install the llmverse package:

```python
pip install packaging wheel torch

```
```python
pip install llmverse==0.1.3

```


# Verifying the Installation:

- ### To check the installed version of llmverse:
```python
import llmverse

print(llmverse.__version__)

```


- ### To see all avilable modules in llmverse package:

```python
import llmverse

print(llmverse.__all__)

```


- ### To see all deatils of a single module in llmverse package:

```python
import llmverse

# See details of load_model module
print(llmverse.__doc__["load_model"])

# OR, see details of chat module
print(llmverse.__doc__["chat"])

# OR, see details of finetune_llm module
print(llmverse.__doc__["finetune_llm"])

# And same for other modules. 

```


# Example of How to Download Any LLM Using llmverse (Skip if already downloaded)

#### Huggingface token is required for some models, and only needs to be provided once per user. You can find your access token [here](https://huggingface.co/settings/tokens).

```python
from llmverse import download_hf_model


# Download the model from HuggingFace to a local folder (Skip if already downloaded).
download_hf_model(
    model_id="microsoft/Phi-3.5-mini-instruct", 
    local_dir="Phi-3.5-mini", 
    hf_token="your_huggingface_read_token"
)

# OR, if you have already logged in using huggingface token previously.
download_hf_model(
    model_id="microsoft/Phi-3.5-mini-instruct", 
    local_dir="Phi-3.5-mini"
)

```


# Example of How to Run Any LLM Using llmverse

```python
from llmverse import download_hf_model, load_model, get_response


# Step 1: Download the model from HuggingFace to a local folder (Skip if already downloaded).
download_hf_model(model_id="microsoft/Phi-3.5-mini-instruct", local_dir="Phi-3.5-mini")


# Step 2: Quantize and load the model.
# If you receive any warning related to Flash Attention, you can use the parameter `use_flash_attn=True`.

model, tokenizer = load_model(model_path="Phi-3.5-mini", optimize="4-bit", device="auto", use_flash_attn=True)


# Step 3: Generate a response using the model.
response = get_response(
    model,
    tokenizer,
    prompt="Name the oceans that surround India."
)
print(response)

# OR, you can use additional parameters to control the model's output. For example:
response = get_response(
    model,
    tokenizer,
    prompt="Name the oceans that surround India.",
    max_new_tokens = 500,
    temperature = 0.1,
    top_p = 0.9,
    repetition_penalty = 1.2
)
print(response)

```


# Example of How to Quantize any LLM and Get Response Using llmverse
```python
from llmverse import download_hf_model, load_model, get_response


# Step 1: Download the model from HuggingFace to a local folder (Skip if already downloaded).
download_hf_model(model_id="mistralai/Mistral-7B-Instruct-v0.3", local_dir="Mistral-v0.3")


# Step 2: Load the model (choose one of the following options based on your quantization preference):
# If you receive any warning related to Flash Attention, you can use the parameter `use_flash_attn=True`.

# For 4-bit quantization:
model, tokenizer = load_model(model_path="Mistral-v0.3", optimize="4-bit", device="auto")

# OR, for 8-bit quantization:
model, tokenizer = load_model(model_path="Mistral-v0.3", optimize="8-bit", device="auto")

# OR, for 16-bit quantization:
model, tokenizer = load_model(model_path="Mistral-v0.3", optimize="16-bit", device="auto")

# OR, for full-size model:
model, tokenizer = load_model(model_path="Mistral-v0.3", optimize=None, device="auto")


# Step 3: Generate a response using the model.
response = get_response(
    model,
    tokenizer,
    prompt="Solve this equation 2x + 3 = 7"
)
print(response)

```


# Example of How to Chat With Any LLM Using llmverse

```python
from llmverse import download_hf_model, load_model, prepare_pipeline, chat


# Step 1: Download the model from HuggingFace to a local folder (Skip if already downloaded).
download_hf_model(model_id="mistralai/Mistral-7B-Instruct-v0.3", local_dir="Mistral-v0.3")


# Step 2: Quantize and load the model.
model, tokenizer = load_model(model_path="Mistral-v0.3", optimize="4-bit", device="auto")


# Step 3: Load the pipeline.
text_gen_pipe, generation_args = prepare_pipeline(
    model,
    tokenizer,
    max_new_tokens = 500
)


# Step 4: Chat with the model. Enter 'quit' or 'exit' to end the conversation.

# Initialize messages
messages = None

# Loop for real-time user input
while True:
    # Take input from the user
    prompt = input("You: ")

    # If the user wants to quit the chat
    if prompt.lower() in ['exit', 'quit']:
        print("Ending chat.")
        break

    # Send the chat request
    messages = chat(
        text_gen_pipe,
        generation_args,
        prompt=prompt,
        messages=messages
    )

    # Print the AI's response
    print("AI:", messages[-1]["content"])

```


# Example of How to Finetune Any LLM Using llmverse

```python
import pandas as pd
from llmverse import download_hf_model, load_model, llm_data_process


# Step 1: Download the model from HuggingFace to a local folder (Skip if already downloaded).
download_hf_model(model_id="meta-llama/Meta-Llama-3.1-8B-Instruct", local_dir="Llama-3.1")


# Step 2: Quantize and load the model.
model, tokenizer = load_model(model_path="Llama-3.1", optimize="4-bit", device="auto")


# Step 3: Load and process data.
data = pd.read_csv("sample_data.csv")

df = llm_data_process(
    tokenizer, 
    data, 
    df_category="not-qa", 
    feature_cols=["feature columns"],
    target_cols=["target columns"], 
    user_prompt="user prompt"
)
print(df.head())

```


#### You can use Wandb to see realtime training details. If you have already logged in previously, this is not required. You can find your wandb key [here](https://wandb.ai/authorize).


```python
from llmverse import find_linear_layers, finetune_llm


# Step 4: Finetune the LLM using QLoRA Technique
linear_layers = find_linear_layers(model)

# Without Wandb, you can still view the training details after the process is fully completed by using the logs.
model_ft, trainer, logs = finetune_llm(
            model=model,
            tokenizer=tokenizer,
            target_modules=linear_layers["self_attn"],
            lora_rank=32,
            df=df,
            validation_percent=20,
            max_steps=25,
            epochs=5,
            learning_rate=2e-4,
            output_dir_name="ft_weights_dir"
        )

# OR, use Wandb to see realtime training details
model_ft, trainer, logs = finetune_llm(
            model=model,
            tokenizer=tokenizer,
            target_modules=linear_layers["self_attn"],
            lora_rank=32,
            df=df,
            validation_percent=20,
            max_steps=25,
            epochs=5,
            learning_rate=2e-4,
            output_dir_name="ft_weights_dir",
            use_wandb=True,
            wandb_key="your_wandb_key"
        )

```

```python
import matplotlib.pyplot as plt


# Step 5: Plot training and evaluation losses

# Extract losses from logs
training_loss = [x['loss'] for x in logs if 'loss' in x]
eval_loss = [x['eval_loss'] for x in logs if 'eval_loss' in x]
# Plot
plt.figure(figsize=(8, 4))
plt.plot(training_loss, label='Training Loss')
plt.plot(eval_loss, label='Validation Loss', marker='o')
plt.xlabel('Evaluation Steps')
plt.ylabel('Loss')
plt.title('Training and Validation Loss Across Epochs')
plt.legend()
plt.grid(True)

# Save the plot to a file
plt.savefig("loss_plot.jpg")

# Show the plot
plt.show()

```

```python
from llmverse import get_response


# Step 6: Test the finetuned LLM.
response = get_response(
    model_ft,
    tokenizer,
    prompt="user query"
)
print(response)

```


# Example of How to Load any Saved Fine-Tuned LLM Using llmverse

```python
from llmverse import load_finetuned_model, get_response


# Step 1: Load a saved finetuned LLM
model_ft, tokenizer = load_finetuned_model(
    base_model_path="Llama-3.1",
    checkpoint_path=f"{output_dir_name}/checkpoint-{max_steps}",
    optimize="4-bit",    
    device="auto",
)


# Step 2: Test the loaded finetuned LLM.
response = get_response(
    model_ft,
    tokenizer,
    prompt="user query"
)
print(response)

```