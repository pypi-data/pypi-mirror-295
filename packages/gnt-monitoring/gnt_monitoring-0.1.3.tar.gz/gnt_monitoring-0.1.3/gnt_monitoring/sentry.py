from logging import getLogger

_logger = getLogger(__name__)


class Sentry():
    """
    Sentry remote logging class
    :param str dsn: Sentry dsn
    :param str env: Sentry env, default: dev
    :returns: None
    """

    def __init__(self, dsn: str, env: str = "dev") -> None:
        """
        """
        try:
            import sentry_sdk
        except ModuleNotFoundError:
            _logger.warning("sentry_sdk not installed")
        else:
            _logger.debug("Initializing sentry")
            sentry_sdk.init(dsn=dsn, environment=env)
