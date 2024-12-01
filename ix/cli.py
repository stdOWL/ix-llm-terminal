from ix.exceptions import IXException
from ix.providers.provider_factory import get_provider
from rich.console import Console
import sys

CONSOLE = Console()


def main():
    try:
        llm = get_provider()
        response = llm.generate("Hello, world!")
        CONSOLE.print(f"[bold green]Response:[/bold green] {response}")
    except IXException as e:
        CONSOLE.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        CONSOLE.print(f"[bold red]Unexpected error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
