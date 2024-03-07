import logging
import colorlog
import os
from datetime import datetime

def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    consol_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
        datefmt='%y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt='%y-%m-%d %H:%M:%S',
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(consol_formatter)

    current_datetime = datetime.now().strftime('%Y-%m-%d')
    log_file_name = f'log_files/logs_{current_datetime}.log'

    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Avoid duplicate messages in the log
    logger.propagate = False

    # Close all handlers associated with the logger
    for handler in logger.handlers:
        handler.close()

    # Remove the previous log file if it exists
    if os.path.exists(log_file_name):
        os.remove(log_file_name)

    return logger
