import pandas as pd
import warnings


# Suppress all warnings
warnings.filterwarnings("ignore")


def llm_data_process(
    tokenizer,
    df: pd.DataFrame,
    df_category: str,
    feature_cols: list,
    target_cols: list,
    user_prompt: str = ""
) -> pd.DataFrame:
    """
    Prepare data for LLM fine-tuning by creating input-output pairs using a chat template.
    
    Args:
        tokenizer (PreTrainedTokenizer): Tokenizer for processing text.
        df (pd.DataFrame): Input data containing user queries and assistant responses.
        df_category (str): {'qa', 'not-qa'} 
            Indicates whether the task is question-answering ('qa') or another type of task ('not-qa').
        feature_cols (list): List of column names containing the model's input.
        target_cols (list): List of column names containing the assistant's responses.
        user_prompt (str): User's instruction to guide the LLM in understanding the relationship between features and the target (optional).

    Returns:
        pd.DataFrame: A DataFrame with formatted text for fine-tuning.
    """

    def not_qa_chat_template(row):
        input_data = ""
        target_data = ""

        for k, v in row.items():
            if k not in target_cols:
                input_data += f", {k}: {v}"
            else:
                target_data += f", {k}: {v}"

        input_data = input_data[1:].strip()
        target_data = target_data[1:].strip()
        messages = [
            {"role": "user", "content": f"{user_prompt}\n{input_data}".strip()},
            {"role": "assistant", "content": target_data}
        ]
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)

    def qa_chat_template(row):
        input_data = ""
        target_data = ""

        for k, v in row.items():
            if k not in target_cols:
                input_data += f", {v}"
            else:
                target_data += f", {v}"

        input_data = input_data[1:].strip()
        target_data = target_data[1:].strip()
        messages = [
            {"role": "user", "content": f"{user_prompt}\n{input_data}".strip()},
            {"role": "assistant", "content": target_data}
        ]
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)

    # Apply the appropriate chat template based on the category
    if df_category == 'not-qa':
        df['text'] = df[feature_cols + target_cols].apply(not_qa_chat_template, axis=1)
    elif df_category == 'qa':
        df['text'] = df[feature_cols + target_cols].apply(qa_chat_template, axis=1)
    else:
        raise ValueError("Invalid df_category. Choose either 'qa' or 'not-qa'.")

    return df