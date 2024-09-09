import logging
from gnt_monitoring.constants import DEFAULT_LOG_FORMAT


def init_logger(
        name: str = "gnt_monitoring",
        level: str = "info",
        format: str = DEFAULT_LOG_FORMAT,
        console: bool = True) -> None:
    """
    Setup logger for this tool

    params:
    :param str name: Logger name
    :param str level: Logging level, default: info
    :param str format: Logging format string
    :param bool console: Add console handler to the main logger

    raises:
    :raises ValueError: For level if it's not available

    return:
    :return: None
    """
    available_log_levels = list(logging._nameToLevel.keys())[:-1]
    if level.upper() not in available_log_levels:
        raise ValueError(f"Logging level: {level} not available to be set")
    set_level = logging.getLevelName(level.upper())
    log_format = logging.Formatter(format if format else DEFAULT_LOG_FORMAT)
    logger = logging.getLogger(name)
    logger.setLevel(set_level)
    if bool(console):
        con_logger = logging.StreamHandler()
        con_logger.setFormatter(log_format)
        con_logger.setLevel(set_level)
        logger.addHandler(con_logger)
