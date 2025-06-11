import os
import logging

def setup_loggers():
    log_dir = os.path.join(os.getcwd(), "logFiles")
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("BeldenLogger")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger  # Prevent adding handlers multiple times

    error_handler = logging.FileHandler(os.path.join(log_dir, "error.log"), mode='w')
    error_handler.setLevel(logging.ERROR)

    warning_handler = logging.FileHandler(os.path.join(log_dir, "warning.log"), mode='w')
    warning_handler.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    error_handler.setFormatter(formatter)
    warning_handler.setFormatter(formatter)

    logger.addHandler(error_handler)
    logger.addHandler(warning_handler)

    return logger
