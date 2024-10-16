import os
import argparse
from dotenv import load_dotenv

from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress
from simple_term_menu import TerminalMenu

from arise.utils import change_directory
from arise.poetry_utils import get_python_versions, create_poetry_project
from arise import github_utils
from arise.config import ENV_FOLDER


console = Console()
visibility_options = ["public", "private"]
python_versions = get_python_versions()
COLORS = {
    "primary": "#FF6F61",
    "secondary": "#9E9E9E",
    "success": "#28a745",
    "failure": "#8B0000",
    "form": "#00FFFF",
}

load_dotenv(dotenv_path=os.path.join(ENV_FOLDER, ".env"))


def main():
    parser = argparse.ArgumentParser(description="Arise command line tool.")
    parser.add_argument("--login", action="store_true", help="Login to Github.")

    args = parser.parse_args()

    if args.login:
        login()
    else:
        run()


def run():
    project = dict()

    console.print(Markdown("# **Welcome To Arise**", style=COLORS["primary"]))
    if not os.getenv("GITHUB_ACCESS_TOKEN") or not os.getenv("GITHUB_USERNAME"):
        console.print(Markdown("**You must set up your GitHub credentials first.**"))
        exit()

    console.print(Markdown("### Project Setup", style=COLORS["secondary"]))
    # Get the name of the project
    while not project.get("name", None):
        console.print("name: ", style=COLORS["form"], end="")
        project["name"] = input()

    # Get the description of the project
    console.print("description: ", style=COLORS["form"], end="")
    project["description"] = input()

    # Get the visibility of the project
    console.print("visibility:", style=COLORS["form"])
    visibility_index = TerminalMenu(visibility_options).show()
    console.print(visibility_options[visibility_index])
    project["private"] = True if visibility_index == 1 else False

    # Get the Python version to use
    console.print("python version:", style=COLORS["form"])
    python_index = TerminalMenu(list(zip(*python_versions))[0]).show()
    console.print(list(zip(*python_versions))[0][python_index])
    project["python"] = python_versions[python_index]

    # Get the Path of the project
    console.print("path: ", style=COLORS["form"], end="")
    project["path"] = os.path.abspath(input())
    # Choose the directory of projects
    change_directory(
        os.path.expanduser("~") if not project["path"] else project["path"]
    )

    progress = Progress()
    progress.start()

    console.print(Markdown("\n\n\n### Project Creation", style=COLORS["secondary"]))

    # Create a poetry project
    create_poetry_project(progress, project)
    # Init git and commit the first changes
    github_utils.init_git(progress)
    # Create a github repo and push project to it
    github_utils.push_to_github(progress, project)

    progress.stop()


def login():
    TRIES_LIMIT = 3

    credentials = dict()
    tries_count = 0

    console.print(Markdown("# **Welcome To Arise**", style=COLORS["primary"]))
    console.print(Markdown("### Github Setup", style=COLORS["secondary"]))

    while (not credentials.get("GITHUB_USERNAME", None)) and tries_count <= TRIES_LIMIT:
        tries_count += 1
        console.print("username: ", style=COLORS["form"], end="")
        credentials["GITHUB_USERNAME"] = input()

    while (
        not credentials.get("GITHUB_ACCESS_TOKEN", None) and tries_count <= TRIES_LIMIT
    ):
        tries_count += 1
        console.print("access token: ", style=COLORS["form"], end="")
        credentials["GITHUB_ACCESS_TOKEN"] = input()

    if not credentials.get("GITHUB_ACCESS_TOKEN") or not credentials.get(
        "GITHUB_USERNAME"
    ):
        console.print("Error: ", end="", style=COLORS["failure"])
        print("Missing GitHub credentials.")
    else:
        if not github_utils.save_github_credentials(credentials):
            console.print("Error: ", end="", style="#8B0000")
            print("Saving credentials went wrong.")

        console.print("Success: ", end="", style=COLORS["success"])
        print("Credentials saved.")


if __name__ == "__main__":
    main()
