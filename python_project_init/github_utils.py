import os

from dotenv import load_dotenv
from github import Github
from github import Auth
from rich.progress import Progress

from utils import run_command

load_dotenv()
auth = Auth.Token(os.getenv("GITHUB_ACCESS_TOKEN"))


def create_github_repo(name: str, description: str = "", private: bool = False):
    github_client = Github(auth=auth)
    try:
        github_client.get_user().create_repo(
            name=name, description=description, private=private
        )
    except Exception as e:
        print(f"Failed to create a repo with that name due to:\n{e}")
    github_client.close()


def init_git(progress: Progress):
    task = progress.add_task("[blue]Setting up Git...", total=100)

    # Initialize Git repository
    output, error = run_command("git init")
    if error:
        print(f"Error initializing Git repository: {error}")
        return
    progress.update(task, advance=25.0)

    # Create a .gitignore file
    with open(".gitignore", "w") as f:
        f.write("*.pyc\n__pycache__\n.vscode\n.idea\n")
    progress.update(task, advance=25.0)

    # Add all files to staging area
    output, error = run_command("git add .")
    if error:
        print(f"Error adding files to staging area: {error}")
        return
    progress.update(task, advance=25.0)

    # Commit changes
    output, error = run_command('git commit -m "Initial commit"')

    if error:
        print(f"Error committing changes: {error}")
        return
    progress.update(task, advance=25.0)


def push_to_github(progress: Progress, project: dict):
    task = progress.add_task("[red]Pushing project to Github...", total=100)

    # Create a github repo
    create_github_repo(project["name"], project["description"], project["private"])
    progress.update(task, advance=50.0)

    # Renaming current branch to main
    output, error = run_command("git branch -M main")
    if error:
        print(f"Error renaming current branch: {error}")
        return
    progress.update(task, advance=10.0)

    # Add the remote repo to the local git
    output, error = run_command(
        f"git remote add origin https://github.com/{os.getenv('GITHUB_USERNAME')}/{project['name']}.git"
    )
    if error:
        print(f"Error adding remote repo to local git: {error}")
        return
    progress.update(task, advance=10.0)

    # Push changes to Github
    output, error = run_command("git push -u origin main")
    if error:
        print(f"Error pushing changes to github: {error}")
        return
    progress.update(task, advance=30.0)
