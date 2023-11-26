import logging

from app.configs import LOGGER_LEVEL

ROOT_FORMATTER = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def logger_config() -> None:
    logger = logging.getLogger('root')
    logger.setLevel(level=LOGGER_LEVEL)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(ROOT_FORMATTER))
    logger.addHandler(handler)
