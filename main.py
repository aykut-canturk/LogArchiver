import time
import logging
from app.utils import zip_and_delete_logs, prepare_logging, log, get_params


def __run():
    log("Operation is starting...")

    log("Binding params...")
    dirs_to_search, archive_threshold_days = get_params()
    log("Params are bound.")

    if not dirs_to_search or len(dirs_to_search) == 0:
        raise ValueError("dirs_to_search param variable is not set.")

    time_threshold = time.time() - (archive_threshold_days * 24 * 60 * 60)

    for d in dirs_to_search:
        log(f"Searching in {d} directory...")
        zip_and_delete_logs(d, time_threshold)

    log("Operation is completed.")


if __name__ == "__main__":
    prepare_logging()
    try:
        __run()
    except Exception as e:
        logging.exception(e)
        raise e
