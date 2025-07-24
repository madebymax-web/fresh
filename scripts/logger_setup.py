import logging
import os

def setup_logger(log_file, level=logging.DEBUG):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Clear old handlers to prevent duplication
    if logger.hasHandlers():
        logger.handlers.clear()

    # File handler (with timestamp, level, etc.)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler (just the message, no timestamp or level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')  # Just the message
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger
