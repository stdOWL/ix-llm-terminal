import subprocess
from pathlib import Path
from typing import Optional

from huggingface_hub import ModelInfo
from rich.console import Console
from halo import Halo
import questionary
import huggingface_hub

# Constants
LLAMA_REPO = "https://github.com/ggerganov/llama.cpp"
LLAMA_CPP_DIR = Path("./llama.cpp")  # Path to the llama.cpp directory
# Rich console for styled outputs
console = Console()

# List of available models for LLaMA
MODELS = list(huggingface_hub.list_models(author="lmsys"))


def is_llama_setup_complete():
    """
    Check if the LLaMA setup is complete by verifying required directories and files.

    Returns:
        bool: True if setup is complete, False otherwise.
    """
    with Halo(text="Checking LLaMA setup...", spinner="dots") as spinner:
        # Check if the llama.cpp directory exists
        if not LLAMA_CPP_DIR.exists() or not LLAMA_CPP_DIR.is_dir():
            spinner.warn("llama.cpp directory is missing.")
            console.print("[bold red]Error:[/bold red] The llama.cpp directory was not found.")
            return False

        return True


def is_git_installed():
    """
    Check if Git is installed on the system.

    Returns:
        bool: True if Git is installed, False otherwise.
    """
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False


def clone_repository():
    """
    Clone the llama.cpp repository or provide instructions if Git is missing.
    """
    if not is_git_installed():
        console.print(
            "[bold red]Error: Git is not installed on your system.[/bold red]\n"
            "Please install Git or manually download the llama.cpp repository from:\n"
            "[blue underline]https://github.com/ggerganov/llama.cpp[/blue underline]"
            f" and place it to {LLAMA_CPP_DIR}."
        )
        raise SystemExit("Git is required for this setup.")

    if LLAMA_CPP_DIR.exists():
        console.print("[bold yellow]Updating llama.cpp repository...[/bold yellow]")
        with Halo(text="Pulling latest changes", spinner="dots"):
            subprocess.run(["git", "-C", str(LLAMA_CPP_DIR), "pull"], check=True)
    else:
        console.print("[bold yellow]Cloning llama.cpp repository...[/bold yellow]")
        with Halo(text="Cloning repository", spinner="dots"):
            subprocess.run(["git", "clone", LLAMA_REPO], check=True)


def ask_for_model_choice() -> Optional[ModelInfo]:
    """
    Ask the user to choose a model for LLaMA using an interactive arrow-based selection.

    Returns:
        str: The chosen model name.
    """

    console.print("[bold yellow]Select a model for LLaMA:[/bold yellow]")

    model_choice = questionary.select(
        "Choose a model:",
        choices=[model.id for model in MODELS]
    ).ask()

    if model_choice is None:
        console.print("[bold red]Error: Model selection is required. Exiting setup.[/bold red]")
        raise SystemExit("Model selection required")

    console.print(f"[bold green]You selected: {model_choice}[/bold green]")
    return next((model for model in MODELS if model.id == model_choice), None)


def download_model_files(model_info: ModelInfo):
    """
    Download the selected model for LLaMA.

    Args:
        model (str): The model name to download.
    """
    console.print("[bold yellow]Downloading model files...[/bold yellow]")
    with Halo(text="Downloading model files", spinner="dots"):
        huggingface_hub.snapshot_download(repo_id=model_info.id, local_dir=f"{LLAMA_CPP_DIR}/models/{model_info.id}",
                                          revision="main")
    console.print("[bold green]Model files downloaded successfully![/bold green]")


def setup_llama():
    """
    Setup the LLaMA environment by cloning the repository and checking the required files.
    """
    console.print("[bold yellow]Setting up LLaMA environment...[/bold yellow]")
    if is_git_installed() is False:
        console.print(f"[bold red]Git is not installed on your system. Install Git and try again or manually download "
                      f"the llama.cpp repository from"
                      f"{LLAMA_REPO}[/bold red]")
        return

    clone_repository()
    model = ask_for_model_choice()
    if model is None:
        console.print("[bold red]Error: Model choice is required.[/bold red]")
        return

    download_model_files(model)

    if is_llama_setup_complete():
        console.print("[bold green]LLaMA setup is complete![/bold green]")
    else:
        console.print("[bold red]LLaMA setup failed.[/bold red]")
