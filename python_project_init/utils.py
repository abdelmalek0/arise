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


def change_directory(path: str):
    try:
        os.chdir(path)
    except OSError as e:
        print(f"Error changing to directory {path}: {e}")
        return
