__version__ = "1.5.17"

import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that applies colors to log level names.
    Uses the colorama library to apply different colors to different log levels.
    """

    COLORS = {
        "DEBUG": Fore.LIGHTCYAN_EX,
        "INFO": Fore.LIGHTGREEN_EX,
        "WARNING": Fore.LIGHTYELLOW_EX,
        "ERROR": Fore.LIGHTRED_EX,
        "CRITICAL": Fore.LIGHTMAGENTA_EX,
    }

    def __init__(self, fmt=None, datefmt=None, style="%"):
        """
        Initialize the ColoredFormatter.
        """
        super().__init__(fmt or "%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt, style)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text with colored log level.
        """
        # Apply color to the log level name
        record.levelname = f"{self.COLORS.get(record.levelname, '')}{record.levelname}{Style.RESET_ALL}"
        formatted_message = super().format(record)

        # Handle exception information if present
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                formatted_message += "\n" + record.exc_text

        return formatted_message

class CustomLogger:
    """
    A custom logger class to provide colored logging functionality.
    """
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    _default_level = INFO
    _loggers = {}

    @classmethod
    def get_logger(cls, name: str, level: str = None) -> logging.Logger:
        """
        Get a logger with the specified name and level.
        """
        if name not in cls._loggers:
            logger = logging.getLogger(name)

            # Determine the log level
            log_level = getattr(cls, level.upper(), cls._default_level) if level else cls._default_level

            # Set the logger's level
            logger.setLevel(log_level)

            formatter = ColoredFormatter()

            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            ch.setFormatter(formatter)

            logger.addHandler(ch)

            cls._loggers[name] = logger

        return cls._loggers[name]

    @classmethod
    def set_default_level(cls, level: int):
        """
        Set the default logging level for all loggers.
        """
        cls._default_level = level
        # Update existing loggers
        for logger in cls._loggers.values():
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)
            logger.info("Logger '%s' level set to %s", logger.name, logging.getLevelName(level))

        logging.info("Default logging level set to %s", logging.getLevelName(level))

# Code Output Complete.