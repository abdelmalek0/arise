import os

from dotenv import load_dotenv
from github import Github
from github import Auth
from rich.progress import Progress

from arise.utils import run_command
from arise.config import ENV_FOLDER


load_dotenv(dotenv_path=os.path.join(ENV_FOLDER, ".env"))


def save_github_credentials(credentials: dict):
    try:
        # Check if the folder exists, create it if it doesn't
        os.makedirs(ENV_FOLDER, exist_ok=True)

        # Define the file path where the credentials will be saved
        file_path = os.path.join(ENV_FOLDER, ".env")

        # Write the credentials to the .env file
        with open(file_path, "w") as f:
            for key, value in credentials.items():
                f.write(f"{key}={value}\n")

        return True
    except Exception as _:
        return False


def create_github_repo(name: str, description: str = "", private: bool = False):
    github_client = Github(auth=Auth.Token(os.getenv("GITHUB_ACCESS_TOKEN")))
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
