import warnings
import os
import subprocess
import sys
from huggingface_hub import login


# Suppress all warnings
warnings.filterwarnings("ignore")


def install_huggingface_hub():
    """Ensure the huggingface_hub package with CLI extras is installed."""
    try:
        import huggingface_hub  # Import to check if it's installed
    except ImportError:
        print("huggingface_hub not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "huggingface_hub[cli]"])
        print("huggingface_hub installed successfully.")


def login_huggingface(hf_token: str) -> None:
    """
    Log in to HuggingFace using the provided token.

    Args:
        hf_token (str): Hugging Face token for authentication.

    Raises:
        RuntimeError: If there is an error during HuggingFace login.
    """
    try:
        login(token=hf_token)
    except Exception as e:
        raise RuntimeError(f"Login failed. Please ensure you have a valid HuggingFace account and try again. Error: {e}") from e


def prepare_local_directory(local_dir: str):
    """
    Prepare the local directory where the model will be downloaded.

    Args:
        local_dir (str): The local directory path.
        
    Returns:
        bool: True if the directory is prepared and ready for download, False if it contains files.
    """
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        print(f"Created directory '{local_dir}'.")
    return True

def execute_model_download(model_id: str, local_dir: str):
    """
    Execute the download of the model using huggingface-cli.

    Args:
        model_id (str): The name of the model to download.
        local_dir (str): The directory where the model will be saved.
    """
    command = [
        "huggingface-cli", "download", model_id, 
        "--local-dir", local_dir, 
        "--local-dir-use-symlinks", "False"
    ]
    
    subprocess.run(command, check=True)
    print(f"Model '{model_id}' downloaded successfully to '{local_dir}'.")

def download_hf_model(model_id: str, local_dir: str, hf_token: str = None):
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
    """
    # Prepare the local directory
    if not prepare_local_directory(local_dir):
        return
    
    try:
        # Try to execute the model download, assuming the user is already logged in
        execute_model_download(model_id, local_dir)
    except subprocess.CalledProcessError as e:
        if hf_token is not None:
            # Ensure the huggingface_hub is installed
            install_huggingface_hub()
            
            # If the download fails, attempt to log in and retry the download
            login_huggingface(hf_token)
            
            try:
                # Retry the download after successful login
                execute_model_download(model_id, local_dir)
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while downloading the model after login: {e}")
                raise
        else:
            print("\nHuggingface read token required to download the model.\nYou can find your access token by going to this link: https://huggingface.co/settings/tokens\n")
