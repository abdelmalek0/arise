import os
import subprocess


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    output = output.decode("utf-8").strip()
    error = error.decode("utf-8").strip()

    # Check if the command succeeded
    if process.returncode == 0:
        # Command was successful, return only output
        return output, None
    else:
        # Command failed, return both output and error
        return output, error


def change_directory(path: str) -> None:
    try:
        os.chdir(path)
    except OSError as e:
        print(f"Error changing to directory {path}: {e}")
        return


def create_arise_script(script_name="arise", install_path="/usr/local/bin"):
    script_content = f"""#!/bin/bash
# Run the 'arise' command using Poetry
poetry run {script_name}
"""
    script_file_path = os.path.join(os.getcwd(), script_name)

    with open(script_file_path, "w") as script_file:
        script_file.write(script_content)

    os.chmod(script_file_path, 0o755)

    if os.path.exists(install_path):
        output, error = run_command(f"sudo cp {script_file_path} {install_path}")
        if error:
            print(f"Error while copying script: {error}")
        else:
            print(f"{script_name} installed to {install_path}.")
    else:
        print(f"{install_path} does not exist. Run it from {script_file_path}.")
