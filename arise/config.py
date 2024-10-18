import os
import logging

ENV_FOLDER = os.path.expanduser("~/.config/arise/")
LOGS_FILE = os.path.expanduser("~/.config/arise/app.log")


def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger that writes log messages to a specified file.

    :param name: Name of the logger
    :param log_file: File to write logs to
    :param level: Logging level (default is INFO)
    :return: Configured logger
    """
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a file handler to log messages to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Create a formatter and set it for the file handler
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


logger = setup_logger("arise", LOGS_FILE, logging.DEBUG)
