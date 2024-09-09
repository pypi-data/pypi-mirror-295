import os
import shutil
import subprocess
from InquirerPy import inquirer
from rich.console import Console
from rich.panel import Panel


console = Console()

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

FRAMEWORK_TEMPLATES = {
    'Django': os.path.join(BASE_DIR, 'templates', 'django_template'),
    'DRF': os.path.join(BASE_DIR, 'templates', 'restframework_template'),
    'FastAPI': os.path.join(BASE_DIR, 'templates', 'fastapi_template'),
    'Flask': os.path.join(BASE_DIR, 'templates', 'flask_template'),
}

DRF_TEMPLATES = {
    'With Oauth': os.path.join(BASE_DIR, 'templates', 'restframework_with_oauth_template'),
    'Without Oauth': os.path.join(BASE_DIR, 'templates', 'restframework_template'),
}

FRAMEWORK_STYLES = {
    'Django': '[bold green]Django[/bold green]',
    'DRF': '[bold]DRF[/bold]',
    'FastAPI': '[bold blue]FastAPI[/bold blue]',
    'Flask': '[bold red]Flask[/bold red]',
}


def ask_user_choice():
    choices = list(FRAMEWORK_TEMPLATES.keys())
    selected_framework = inquirer.select(
        message="Choose a framework to implement your project:",
        choices=choices,
        pointer="=>",
        instruction="(use arrows to select)"
    ).execute()

    if selected_framework == 'DRF':
        drf_options = list(DRF_TEMPLATES.keys())
        selected_option = inquirer.select(
            message="Choose an option:",
            choices=drf_options,
            pointer="=>",
            instruction="(use arrows to select)"
        ).execute()
        selected_framework = selected_option

    return selected_framework


def install_dependencies(project_path):
    requirements_file = os.path.join(project_path, 'requirements.txt')
    if os.path.isfile(requirements_file):
        subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', '-r', requirements_file])


def create_project_structure(selected_framework, project_name):
    if selected_framework in DRF_TEMPLATES:
        template_path = DRF_TEMPLATES[selected_framework]
    else:
        template_path = FRAMEWORK_TEMPLATES[selected_framework]
    project_path = os.path.join(os.getcwd(), project_name)
    shutil.copytree(template_path, project_path)
    with console.status(
            "[bold][yellow]Installing dependencies from requirements.txt...[/yellow][/bold]",
            spinner='monkey'
    ):
        install_dependencies(project_path)

    success_message = (
        f'Project: "{project_name}" for framework: "{FRAMEWORK_STYLES[selected_framework]}" successfully created!'
    )
    console.print(Panel(success_message, title="Success", title_align="left"))


def main():
    selected_framework = ask_user_choice()
    project_name = console.input('[bold][blue]Enter your project name: [/blue][/bold]')
    create_project_structure(selected_framework, project_name)


if __name__ == '__main__':
    main()
