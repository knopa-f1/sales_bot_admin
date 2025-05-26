import logging
import logging.config

from app.settings import DEBUG


def setup_logging() -> None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": "DEBUG" if DEBUG is True else "INFO",
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "logs/app.log",
                "formatter": "standard",
                "level": "DEBUG" if DEBUG is True else "INFO",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    }

    logging.config.dictConfig(logging_config)
