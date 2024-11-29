import subprocess
from pathlib import Path
from rich.console import Console
from halo import Halo
import questionary

# Constants
LLAMA_REPO = "https://github.com/ggerganov/llama.cpp"
LLAMA_CPP_DIR = Path("./llama.cpp")  # Path to the llama.cpp directory
# Rich console for styled outputs
console = Console()

MODELS = [
    {
        "name": "llama-7b",
        "description": "LLaMA 7B model",
        "default": True,
        "dir": "models/7B",
        "files": [
            "pytorch_model-00001-of-00002.bin",
            "pytorch_model-00002-of-00002.bin",
            "tokenizer.model",
            "config.json",
        ],
        "urls": [
            f"https://huggingface.co/huggyllama/llama-7b/resolve/main/{file}"
            for file in [
                "pytorch_model-00001-of-00002.bin",
                "pytorch_model-00002-of-00002.bin",
                "tokenizer.model",
                "config.json",
            ]
        ],
    }
]


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

        # Check if the llama.cpp build is complete (e.g., 'main' binary exists)
        if not (LLAMA_CPP_DIR / "main").exists():
            spinner.warn("llama.cpp build incomplete.")
            console.print(
                "[bold red]Error:[/bold red] The llama.cpp binary ('main') is missing. Build might not be complete.")
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


def ask_for_model_choice():
    """
    Ask the user to choose a model for LLaMA using an interactive arrow-based selection.

    Returns:
        str: The chosen model name.
    """

    console.print("[bold yellow]Select a model for LLaMA:[/bold yellow]")

    model_choice = questionary.select(
        "Choose a model:",
        choices=[model["name"] for model in MODELS],
        default=next((model["name"] for model in MODELS if model.get("default")), "llama-7b"),
    ).ask()

    if model_choice is None:
        console.print("[bold red]Error: Model selection is required. Exiting setup.[/bold red]")
        raise SystemExit("Model selection required")

    console.print(f"[bold green]You selected: {model_choice}[/bold green]")
    return model_choice


def download_model_files(model):
    """
    Download the selected model for LLaMA.

    Args:
        model (str): The model name to download.
    """
    model_info = next((m for m in MODELS if m["name"] == model), None)
    if model_info is None:
        console.print(f"[bold red]Error: Model '{model}' not found.[/bold red]")
        return

    console.print(f"[bold yellow]Downloading model files for {model}...[/bold yellow]")
    with Halo(text="Downloading model files", spinner="dots"):
        for url in model_info["urls"]:
            subprocess.run(["wget", url, "-P", str(LLAMA_CPP_DIR / model_info["dir"])], check=True)


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
