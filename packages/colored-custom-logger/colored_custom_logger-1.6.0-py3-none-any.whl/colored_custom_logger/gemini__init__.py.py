__version__ = "1.5.17"

import logging
from typing import Dict

# Use ANSI escape codes directly for broader compatibility
# from colorama import Fore, Style, init

# Initialize colorama (no longer needed)
# init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that applies colors to log level names.

    This formatter extends the standard logging.Formatter to add color-coding
    to log level names in the output. It uses ANSI escape codes to apply
    different colors to different log levels.

    Attributes:
        COLORS (Dict[str, str]): A dictionary mapping log level names to ANSI color codes.
            - DEBUG: Light Cyan
            - INFO: Light Green
            - WARNING: Light Yellow
            - ERROR: Light Red
            - CRITICAL: Light Magenta
        RESET (str): ANSI code to reset color formatting.
    """

    COLORS: Dict[str, str] = {
        "DEBUG": "\033[96m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m",
    }
    RESET: str = "\033[0m"

    def __init__(self, fmt: str = None, datefmt: str = None, style: str = "%") -> None:
        """
        Initialize the ColoredFormatter.

        This method sets up the formatter with the given format string, date format, and style.
        If no format string is provided, it uses a default format.

        Args:
            fmt (str, optional): A format string for log messages.
                                 Defaults to "%(asctime)s - %(levelname)s - %(name)s - %(message)s".
            datefmt (str, optional): A format string for dates in log messages.
                                     Defaults to None.
            style (str, optional): The style of the format string. Can be '%', '{', or '$'.
                                   Defaults to '%'.
        """
        super().__init__(fmt, datefmt, style)

        self._base_fmt = fmt or "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text.

        This method overrides the standard format method to add color to the log level.
        It creates a new Formatter instance with a colored format string for each record,
        ensuring that the original formatter remains unchanged.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record as a string, with the log level colored
                 according to the COLORS dictionary.
        """
        # Get the color for the log level
        color = self.COLORS.get(record.levelname, "")

        # Apply color to the log level name
        formatted_levelname = f"{color}{record.levelname}{self.RESET}"

        # Create a new formatter with the colored level name
        formatter = logging.Formatter(
            self._base_fmt.replace("%(levelname)s", formatted_levelname),
            self.datefmt,
            self.style,
        )

        # Format the record using the new formatter
        formatted_message = formatter.format(record)

        return formatted_message


class CustomLogger:
    """
    A custom logger class that provides colored logging output and simplifies logger creation.

    This class wraps the standard logging.Logger class to provide a more user-friendly interface
    for creating and configuring loggers. It also adds color-coding to log level names in the output.

    Attributes:
        DEBUG (int): Logging level for debugging messages.
        INFO (int): Logging level for informational messages.
        WARNING (int): Logging level for warning messages.
        ERROR (int): Logging level for error messages.
        CRITICAL (int): Logging level for critical messages.
        _default_level (int): The default logging level for new loggers.
                               Defaults to logging.INFO.
        _loggers (Dict[str, logging.Logger]): A dictionary storing created loggers,
                                             keyed by their names.
    """

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    _default_level: int = INFO
    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(cls, name: str, level: str = None) -> logging.Logger:
        """
        Get a logger with the specified name and level.

        If a logger with the given name already exists, it is returned. Otherwise, a new logger
        is created with the specified name and level, and added to the _loggers dictionary.

        Args:
            name (str): The name of the logger.
            level (str, optional): The logging level for the logger.
                                   Defaults to the default level set by set_default_level.

        Returns:
            logging.Logger: The logger with the specified name and level.
        """
        if name not in cls._loggers:
            logger = logging.getLogger(name)

            # Determine the log level
            if level:
                log_level = getattr(cls, level.upper(), cls._default_level)
            else:
                log_level = cls._default_level

            # Set the logger's level
            logger.setLevel(log_level)

            formatter = ColoredFormatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )

            ch = logging.StreamHandler()
            ch.setLevel(log_level)  # Set the handler's level to match the logger's level
            ch.setFormatter(formatter)

            logger.addHandler(ch)

            cls._loggers[name] = logger

        return cls._loggers[name]

    @classmethod
    def set_default_level(cls, level: int) -> None:
        """
        Set the default logging level for new loggers.

        This method sets the default logging level that will be used for new loggers
        created using the get_logger method. It also updates the level of existing loggers
        and the default logging level.

        Args:
            level (int): The new default logging level.
        """
        cls._default_level = level
        logger = logging.getLogger(__name__)
        logger.info("Logger '%s' level set to %s", __name__, logging.getLevelName(level))

        # Update existing loggers
        for logger in cls._loggers.values():
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)
            logger.info("Logger '%s' level set to %s", logger.name, logging.getLevelName(level))

        # Update default logging level
        # logging.basicConfig(level=level)
        logger.info("Default logging level set to %s", logging.getLevelName(level))