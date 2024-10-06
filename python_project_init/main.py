import os

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress
from simple_term_menu import TerminalMenu

from python_project_init.utils import change_directory
from python_project_init.poetry_utils import get_python_versions, create_poetry_project
from python_project_init.github_utils import init_git, push_to_github

load_dotenv()

console = Console()
visibility_options = ["public", "private"]
python_versions = get_python_versions()
text_color = "#6ab0de"


def main():
    project = dict()

    console.print(
        Markdown("# Welcome To Python Project Initializer\n### Project Setup")
    )

    # Get the name of the project
    while not project.get("name", None):
        console.print("name: ", style=text_color, end="")
        project["name"] = input()

    # Get the description of the project
    console.print("description: ", style=text_color, end="")
    project["description"] = input()

    # Get the visibility of the project
    console.print("visibility:", style=text_color)
    visibility_index = TerminalMenu(visibility_options).show()
    console.print(visibility_options[visibility_index])
    project["private"] = True if visibility_index == 1 else False

    # Get the Python version to use
    console.print("python version:", style=text_color)
    python_index = TerminalMenu(list(zip(*python_versions))[0]).show()
    console.print(list(zip(*python_versions))[0][python_index])
    project["python"] = python_versions[python_index]

    # Get the Path of the project
    console.print("path: ", style=text_color, end="")
    project["path"] = os.path.abspath(input())
    # Choose the directory of projects
    change_directory(
        os.path.expanduser("~") if not project["path"] else project["path"]
    )

    progress = Progress()
    progress.start()

    console.print(Markdown("\n\n\n### Project Creation"))

    # Create a poetry project
    create_poetry_project(progress, project)

    # Init git and commit the first changes
    init_git(progress)
    # Create a github repo and push project to it
    push_to_github(progress, project)

    progress.stop()


if __name__ == "__main__":
    main()
