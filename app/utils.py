import sys
import os
import json
import zipfile
import logging
import re


def get_params(config_file="config.json"):
    """Get the parameters from the config file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"{config_file} not found.")

    with open(config_file, "r", encoding="utf-8") as f:
        params = json.load(f)
        if "DirsToSearch" not in params or "ArchiveThresholdDays" not in params:
            raise ValueError(
                "DirsToSearch or ArchiveThresholdDays not found in config file."
            )
        dirs_to_search = params["DirsToSearch"]
        archive_threshold_days = params["ArchiveThresholdDays"]

        if not isinstance(dirs_to_search, list):
            raise ValueError("DirsToSearch must be a list.")
        if not all(isinstance(d, str) for d in dirs_to_search):
            raise ValueError("All elements of DirsToSearch must be a string.")

        if not isinstance(archive_threshold_days, int):
            raise ValueError("ArchiveThresholdDays must be an integer.")

        return dirs_to_search, int(archive_threshold_days)


def prepare_logging(log_dir=None):
    """Prepare the logging configuration."""
    if not log_dir and len(sys.argv) > 0:
        log_dir = os.path.dirname(sys.argv[0])

    filename = os.path.join(log_dir, "logs.log") if log_dir else "logs.log"

    logging.basicConfig(
        filename=filename, level=logging.DEBUG, format="%(asctime)s %(message)s"
    )


def log(message):
    """Log the message to the console and the log file."""
    logging.info(message)
    print(message)


def zip_and_delete_logs(directory, file_age_limit):
    """Zip and delete the log files older than the file_age_limit."""
    for root, _, files in os.walk(directory):
        for filename in files:
            if re.search(r"(\.log|\.txt)(\.\d+)?$", filename):
                file_path = os.path.join(root, filename)

                # Check if the file is older than the file_age_limit
                if os.path.getmtime(file_path) < file_age_limit:
                    # Zip the file and save it in the same directory
                    zip_file_path = os.path.join(root, f"{filename}.zip")
                    with zipfile.ZipFile(
                        zip_file_path, "w", zipfile.ZIP_DEFLATED
                    ) as zipf:
                        zipf.write(file_path, arcname=filename)
                        log(f"{file_path} zipped.")

                    # Delete the original file
                    os.remove(file_path)
                    log(f"{file_path} deleted.")
