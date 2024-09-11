import logging


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("file.log")
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


def debug(logger, message):
    logger.debug(message)


def info(logger, message):
    logger.info(message)


def warning(logger, message):
    logger.warning(message)


def error(logger, message):
    logger.error(message)


def critical(logger, message):
    logger.critical(message)
