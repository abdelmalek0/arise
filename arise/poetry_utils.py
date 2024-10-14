import os
import re
import subprocess

import toml
from rich.progress import Progress

from arise.utils import run_command
from arise.utils import change_directory


def get_python_versions():
    """Get installed Python versions based on the operating system."""
    versions = list()  # Initialize a set to store unique versions

    if os.name == "nt":  # Windows
        try:
            # Use subprocess to run the 'where python' command
            output = subprocess.check_output(
                ["where", "python"], stderr=subprocess.STDOUT
            ).decode()

            # print(output)
            # Extract Python versions from the output (e.g., Python38, Python312)
            version_matches = re.findall(r"Python(\d+)", output)
            version_paths = [
                path
                for path in output.split("\r\n")
                for version in version_matches
                if version in path
            ]
            # print(version_paths)
            # Format the versions to include the full version (e.g., 3.8, 3.12)
            versions = [
                ("3" + ".".join(version.split("3")), path)
                for version, path in zip(version_matches, version_paths)
            ]

        except subprocess.CalledProcessError as e:
            print("Error listing Python versions:", e.output.decode())
            return []

    else:  # Linux/macOS/WSL
        possible_paths = ["/usr/bin", "/usr/local/bin"]

        for path in possible_paths:
            try:
                for entry in os.listdir(path):
                    if entry.startswith("python"):
                        version_match = re.search(r"python(\d+\.\d+)", entry)
                        if version_match:
                            versions.append(
                                (
                                    version_match.group(0).split("python")[1],
                                    os.path.join(path, entry),
                                )
                            )
            except FileNotFoundError:
                continue  # Ignore if the directory doesn't exist

    return sorted(versions)  # Return sorted list of unique versions


def create_poetry_project(progress: Progress, project: dict):
    task = progress.add_task("[green]Creating poetry project...", total=100)
    # Create a new poetry project
    _, error = run_command(f"{project['python'][1]} -m poetry new {project['name']}")
    if error:
        print(f"Error creating poetry project: {error}")
        exit(1)
    progress.update(task, advance=25.0)

    pyproject_path = project["name"] + "/pyproject.toml"
    with open(pyproject_path, "r") as f:
        pyproject = toml.load(f)

    # Set the project description + py version in the pyproject.toml
    pyproject["tool"]["poetry"]["description"] = project["description"]
    pyproject["tool"]["poetry"]["dependencies"]["python"] = "~" + project["python"][0]

    progress.update(task, advance=25.0)

    with open(pyproject_path, "w") as f:
        toml.dump(pyproject, f)

    # Cd to the poetry project
    change_directory(project["name"])

    _, error = run_command(f"poetry env use {project['python'][1]}")
    if error:
        print(f"Error Using this python version: {error}")
        exit(1)
    # Update poetry lock file
    _, error = run_command(f"{project['python'][1]} -m poetry update")
    if error:
        print(f"Error updating poetry lock file: {error}")
        exit(1)
    progress.update(task, advance=25.0)

    # Create virtual env
    _, error = run_command(f"{project['python'][1]} -m poetry install")
    if error:
        print(f"Error creating virtual environment: {error}")
        exit(1)
    progress.update(task, advance=25.0)
