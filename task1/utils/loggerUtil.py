
import logging
import os

def getLogger(name="app"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger

    log_dir = os.path.join(os.getcwd(), "logFiles")
    os.makedirs(log_dir, exist_ok=True)

    error_handler = logging.FileHandler(os.path.join(log_dir, "error.log"), mode='w')
    error_handler.setLevel(logging.ERROR)

    warning_handler = logging.FileHandler(os.path.join(log_dir, "warning.log"),mode='w')
    warning_handler.setLevel(logging.WARNING)

    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    error_handler.setFormatter(formatter)
    warning_handler.setFormatter(formatter)
    # console_handler.setFormatter(formatter)

    logger.addHandler(error_handler)
    logger.addHandler(warning_handler)
    # logger.addHandler(console_handler)

    return logger
