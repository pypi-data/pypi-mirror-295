from rich.console import Console
from rich.panel import Panel


console = Console()


def main():
    message = (
        '[bold][green]builder-run[/green][/bold]      [bold]Starts collecting the project.[/bold]🏃\n'
        '[bold][red]builder-rebuild[/red][/bold]  [bold]rebuilds the project to another framework.[/bold]🔨\n'
        '[bold]builder--help[/bold]    [bold]help command[/bold]💡'
    )
    console.print(Panel(message, title="Commands", title_align="left"))


if __name__ == '__main__':
    main()
