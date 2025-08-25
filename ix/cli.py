import argparse
import json
import sys
from ix.exceptions import IXException
from ix.providers.provider_factory import get_provider
from rich.console import Console

CONSOLE = Console()


def interactive_shell():
    """
    Launch an interactive shell for querying and tracking commands.
    """
    CONSOLE.print("[bold blue]Launching interactive shell...[/bold blue]")
    # Implement your interactive shell logic here
    CONSOLE.print("[bold green]Interactive shell closed.[/bold green]")


def setup_terminal():
    """
    Reconfigure or set up the terminal again.
    """
    CONSOLE.print("[bold blue]Setting up the terminal...[/bold blue]")
    # Implement terminal setup logic here
    CONSOLE.print("[bold green]Setup completed successfully.[/bold green]")


def fine_tune_model(dataset):
    """
    Fine-tune the model using the provided dataset.

    Args:
        dataset (str): The dataset as a string.
    """
    try:
        llm = get_provider()
        CONSOLE.print("[bold blue]Starting fine-tuning process...[/bold blue]")

        llm.fine_tune(dataset=dataset)
        CONSOLE.print("[bold green]Fine-tuning completed successfully![/bold green]")
    except IXException as e:
        CONSOLE.print(f"[bold red]Fine-tuning error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        CONSOLE.print(f"[bold red]Unexpected error during fine-tuning:[/bold red] {e}")
        sys.exit(1)


def process_tune_input(file_path=None):
    """
    Handle input for fine-tuning from a file or piped input.

    Args:
        file_path (str): The path to the dataset file.
    """
    if file_path:
        try:
            with open(file_path, "r") as f:
                dataset = f.read()

            dataset = dataset.strip().splitlines()
            print(dataset)
        except FileNotFoundError:
            CONSOLE.print(f"[bold red]Error: File not found - {file_path}[/bold red]")
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            CONSOLE.print("[bold red]Error: No piped input detected for fine-tuning.[/bold red]")
            sys.exit(1)
        dataset = sys.stdin.read().strip().splitlines()

    dataset = [json.dumps({
        "messages": [
            {"role": "user", "content": item},
            {"role": "assistant", "content": item}
        ]
    }) for item in dataset]

    fine_tune_model(dataset)


def process_query(prompt=None):
    """
    Process a query and optionally support piped input.

    Args:
        prompt (str): The user-provided query prompt.
    """
    if not prompt:
        if sys.stdin.isatty():
            CONSOLE.print("[bold red]Error: No prompt or piped input provided for query.[/bold red]")
            sys.exit(1)
        prompt = sys.stdin.read().strip()

    try:
        llm = get_provider()
        CONSOLE.print(f"[bold blue]Processing query:[/bold blue] {prompt}")
        response = llm.generate(prompt)
        CONSOLE.print(f"[bold green]Generated Command:[/bold green] {response}")
    except IXException as e:
        CONSOLE.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        CONSOLE.print(f"[bold red]Unexpected error:[/bold red] {e}")
        sys.exit(1)


def main():
    """
    Main entry point for the CLI tool.
    """
    # Use custom parsing to handle non-subcommand prompts
    if len(sys.argv) > 1 and sys.argv[1] not in {"interactive", "help", "setup", "finetune", "query"}:
        # Treat as a direct prompt
        prompt = " ".join(sys.argv[1:])
        process_query(prompt)
        return

    # Otherwise, use argparse for subcommands
    parser = argparse.ArgumentParser(
        description="ix-llm-terminal CLI: A tool for querying, fine-tuning, and managing logs commands."
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # Interactive shell
    subparsers.add_parser(
        "interactive",
        help="Launch an interactive shell which suggests commands and keeps track of them."
    )

    # Help
    subparsers.add_parser(
        "help",
        help="Show the help message."
    )

    # Setup terminal
    subparsers.add_parser(
        "setup",
        help="Setup or reconfigure the terminal."
    )

    # Fine-tune
    finetune_parser = subparsers.add_parser(
        "finetune",
        help="Fine-tune the model using a dataset file or piped input."
    )
    finetune_parser.add_argument(
        "file_path",
        nargs="?",
        help="Path to the dataset file for fine-tuning. If omitted, piped input will be used."
    )

    # Query
    query_parser = subparsers.add_parser(
        "query",
        help="Process a natural language query to generate commands."
    )
    query_parser.add_argument(
        "prompt",
        nargs="?",
        help="The query prompt to process. If omitted, piped input will be used."
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle subcommands
    if args.subcommand == "interactive":
        interactive_shell()
    elif args.subcommand == "help":
        parser.print_help()
    elif args.subcommand == "setup":
        setup_terminal()
    elif args.subcommand == "finetune":
        process_tune_input(args.file_path)
    elif args.subcommand == "query":
        process_query(args.prompt)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
