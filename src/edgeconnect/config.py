import os

# GENERAL
ENV_CLASS = os.environ.get("ENVIRONMENT_TYPE", "DEV")  # DEV | TEST | PROD
DEBUG = bool(ENV_CLASS in ("DEV", "TEST"))

# LOGGING
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DEFAULT_LOG_FORMATTER = "debug" if DEBUG else "default"

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {},
    "formatters": {
        "debug": {
            "format": (
                "LOG:%(levelname)s [ %(asctime)s ] "
                "[ %(filename)s:%(lineno)s ] %(message)s"
            ),
        },
        "default": {
            "format": "LOG:%(levelname)s [ %(asctime)s ] %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": DEFAULT_LOG_FORMATTER,
        },
    },
    "root": {
        "handlers": ["default"],
        "level": LOG_LEVEL if DEBUG else "ERROR",
    },
    "loggers": {
        "edgeconnect": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

# HTTP
SERVER_HOST = os.environ.get("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.environ.get("SERVER_PORT", 8000))
SERVER_CONCURRENCY_LIMIT = int(os.environ.get("SERVER_CONCURRENCY_LIMIT", 10))
ROOT_URI_PATH = os.environ.get("ROOT_URI_PATH", "")
