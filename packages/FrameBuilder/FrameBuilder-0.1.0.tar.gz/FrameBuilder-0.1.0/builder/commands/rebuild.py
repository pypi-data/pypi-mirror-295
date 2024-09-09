import os
import shutil
import subprocess
from rich.console import Console
from rich.panel import Panel

from .run import main as run


console = Console()


def find_project_folder():
    current_directory = os.getcwd()
    for root, dirs, files in os.walk(current_directory):
        if 'requirements.txt' in files:
            return root
    return None


def uninstall_dependencies(project_path):
    requirements_file = os.path.join(project_path, 'requirements.txt')
    if os.path.isfile(requirements_file):
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'uninstall', '-y', '-r', requirements_file])
        console.print("[bold green]Dependencies uninstalled.[/bold green]")


def clear():
    current_directory = os.getcwd()
    console.print("[bold yellow]Clearing project folder...[/bold yellow]")
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if item != 'venv':
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    success_message = (
        '[bold green]Project folder cleared.[/bold green]'
    )
    console.print(Panel(success_message, title="Success", title_align="left"))


def main():
    project_path = find_project_folder()

    if project_path:
        with console.status(
                "[bold][yellow]Uninstalling dependencies from requirements.txt...[/yellow][/bold]",
                spinner='monkey'
        ):
            uninstall_dependencies(project_path)
        clear()
        run()
    else:
        console.print("[bold red]No project folder with requirements.txt.[/bold red]")


if __name__ == '__main__':
    main()
