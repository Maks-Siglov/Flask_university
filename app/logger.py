import logging

from app.configs import LOGGER_LEVEL

ROOT_FORMATTER = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def logger_config() -> None:
    """This function configure logger, it takes logger_level from config, and
    set formatter by provided variable"""
    logger = logging.getLogger("root")
    assert LOGGER_LEVEL
    logger.setLevel(level=LOGGER_LEVEL)
    handler = logging.StreamHandler()
    my_formatter = logging.Formatter(ROOT_FORMATTER)
    handler.setFormatter(my_formatter)
    logger.addHandler(handler)
