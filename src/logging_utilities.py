import logging


def init_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add logging to a file
    file_handler = logging.FileHandler(f'{name}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # add logging to stderr
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
