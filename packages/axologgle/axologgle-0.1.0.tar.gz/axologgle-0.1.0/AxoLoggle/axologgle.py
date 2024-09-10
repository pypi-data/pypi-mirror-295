"""
AxoLoggle - Custom Logging Module

(c) 2024 Axo. All Rights Reserved.
This module provides flexible and customizable logging functionality with color support for various log levels.
Anyone may use this module, but modifications must credit the original author.

Features:
- Custom log levels with dynamic logging functions.
- Color-coded log output for both default and custom log levels.
- Easy-to-use API for enabling/disabling log levels and setting colors.

"""

import logging
from enum import Enum
from typing import List
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


class LogColor(Enum):
    """Enum representing valid color options for log messages, utilizing colorama for terminal color output."""

    RED = Fore.RED
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    YELLOW = Fore.YELLOW
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    LIGHTGREEN = Fore.LIGHTGREEN_EX
    LIGHTBLUE = Fore.LIGHTBLUE_EX
    LIGHTRED = Fore.LIGHTRED_EX
    LIGHTCYAN = Fore.LIGHTCYAN_EX


class LogLevel(Enum):
    """Enum representing standard and custom log levels with specific numerical values."""

    TRACE = 5
    VERBOSE = 7
    DEBUG = 10
    INFO = 20
    NOTICE = 25
    SUCCESS = 28
    WARNING = 30
    ERROR = 40
    ALERT = 45
    CRITICAL = 50


class Logger(logging.Formatter):
    """Custom logger to support multiple log levels and colors for terminal output.

    Handles predefined log levels as well as dynamically added custom levels.
    """

    STYLES = {
        "DEBUG": Fore.CYAN,
        "VERBOSE": Fore.MAGENTA,
        "INFO": Fore.BLUE,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.WHITE + colorama.Back.RED,
        "TRACE": Fore.BLACK + colorama.Back.YELLOW,
        "SUCCESS": Fore.GREEN,
        "NOTICE": Fore.LIGHTBLUE_EX,
        "ALERT": Fore.MAGENTA,
    }

    def __init__(self) -> None:
        """Initializes the logger with basic formatting."""
        super().__init__("%(message)s")

    def format(self, record: logging.LogRecord) -> str:
        """Formats log messages with color and timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        style = self.STYLES.get(record.levelname, Fore.WHITE)
        message = super().format(record)
        if record.levelname == "TRACE":
            return f"{Style.DIM}{timestamp} {Style.RESET_ALL}{style}{record.levelname}{Style.RESET_ALL}   {Fore.LIGHTBLACK_EX} // {Fore.WHITE}{message}"
        return f"{Style.DIM}{timestamp} {Style.RESET_ALL}{style}{record.levelname:<8}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX} // {Fore.WHITE}{message}"

    @staticmethod
    def initialize() -> None:
        """Initializes the logging system with a simple stream handler and default formatter."""
        handler = logging.StreamHandler()
        handler.setFormatter(Logger())
        logging.basicConfig(level=logging.DEBUG, handlers=[handler])

    @staticmethod
    def add_custom_level(name: str, level_num: int, color: LogColor = LogColor.WHITE) -> None:
        """Adds a custom log level and assigns a specific color to it.

        Args:
            name (str): Name of the custom log level.
            level_num (int): Numerical value for the custom log level.
            color (Color): Color enum for log level display.

        Raises:
            ValueError: If the level name or value is invalid.
        """
        if not name or not isinstance(level_num, int):
            raise ValueError(f"Invalid log level name or value: {name}, {level_num}")
        logging.addLevelName(level_num, name.upper())
        Logger.STYLES[name.upper()] = color.value

    @staticmethod
    def set_level_color(level: LogLevel, color: LogColor) -> None:
        """Sets the color for a predefined log level.

        Args:
            level (LogLevel): The log level to set color for.
            color (Color): The color to assign to the log level.
        """
        Logger.STYLES[level.name] = color.value


for level in LogLevel:
    logging.addLevelName(level.value, level.name)


def _log(level_name: str, level_value: int, message: str, *args, **kwargs) -> None:
    """Logs a message at a specific log level."""
    if logging.getLogger().isEnabledFor(level_value):
        logging.getLogger()._log(level_value, message, args, stacklevel=2, **kwargs)


log_trace = lambda msg, *a, **kw: _log("TRACE", LogLevel.TRACE.value, msg, *a, **kw)
log_success = lambda msg, *a, **kw: _log(
    "SUCCESS", LogLevel.SUCCESS.value, msg, *a, **kw
)
log_verbose = lambda msg, *a, **kw: _log(
    "VERBOSE", LogLevel.VERBOSE.value, msg, *a, **kw
)
log_notice = lambda msg, *a, **kw: _log("NOTICE", LogLevel.NOTICE.value, msg, *a, **kw)
log_alert = lambda msg, *a, **kw: _log("ALERT", LogLevel.ALERT.value, msg, *a, **kw)


class AxoLoggle:
    """Main class to manage logging behavior, including custom log levels and color customization."""

    def __init__(self, enabled_levels: List[LogLevel] = None) -> None:
        """Initializes the logging system with custom log levels if provided.

        Args:
            enabled_levels (List[LogLevel], optional): List of log levels to enable on initialization.
        """
        Logger.initialize()
        if enabled_levels:
            self._set_logging_levels(enabled_levels)

    def _log(self, level_name: str, level_value: int, message: str) -> None:
        """Logs a message at a specific log level."""
        _log(level_name, level_value, message)

    info = lambda self, msg: self._log("INFO", LogLevel.INFO.value, msg)
    debug = lambda self, msg: self._log("DEBUG", LogLevel.DEBUG.value, msg)
    warning = lambda self, msg: self._log("WARNING", LogLevel.WARNING.value, msg)
    error = lambda self, msg: self._log("ERROR", LogLevel.ERROR.value, msg)
    critical = lambda self, msg: self._log("CRITICAL", LogLevel.CRITICAL.value, msg)
    trace = lambda self, msg: self._log("TRACE", LogLevel.TRACE.value, msg)
    success = lambda self, msg: self._log("SUCCESS", LogLevel.SUCCESS.value, msg)
    verbose = lambda self, msg: self._log("VERBOSE", LogLevel.VERBOSE.value, msg)
    notice = lambda self, msg: self._log("NOTICE", LogLevel.NOTICE.value, msg)
    alert = lambda self, msg: self._log("ALERT", LogLevel.ALERT.value, msg)

    def set_level(self, level: LogLevel) -> None:
        """Sets the global log level."""
        logging.getLogger().setLevel(level.value)

    def enable_level(self, level: LogLevel) -> None:
        """Enables a specific log level by ensuring it's part of the current logging threshold."""
        logging.getLogger().setLevel(min(logging.getLogger().level, level.value))

    def disable_level(self, level: LogLevel) -> None:
        """Disables a specific log level by raising the logging threshold."""
        if logging.getLogger().level <= level.value:
            logging.getLogger().setLevel(level.value + 1)

    def _set_logging_levels(self, levels: List[LogLevel]) -> None:
        """Enables multiple logging levels based on the provided list."""
        for level in levels:
            self.enable_level(level)

    def set_level_color(self, level: LogLevel, color: LogColor) -> None:
        """Sets the display color for a specific log level."""
        Logger.set_level_color(level, color)

    def create_custom_level(
        self, name: str, value: int, color: LogColor = LogColor.WHITE
    ) -> None:
        """Creates a custom log level with the given name, value, and color.

        Args:
            name (str): Name of the custom log level.
            value (int): Numeric value for the custom log level.
            color (Color): Color enum for log level display.

        Raises:
            ValueError: If invalid log level name or value is provided.
        """
        if not name or not isinstance(value, int) or value < 0:
            raise ValueError(f"Invalid custom log level: {name}, {value}")
        Logger.add_custom_level(name, value, color)
        setattr(
            self,
            name.lower(),
            lambda msg, *a, **kw: _log(name.upper(), value, msg, *a, **kw),
        )

    def remove_custom_level(self, name: str) -> None:
        """Removes a custom log level by name, if it exists.

        Args:
            name (str): The name of the custom log level to remove.

        Raises:
            ValueError: If the custom level does not exist.
        """
        if name.upper() in Logger.STYLES:
            del Logger.STYLES[name.upper()]
            if hasattr(self, name.lower()):
                delattr(self, name.lower())
        else:
            raise ValueError(f"Custom log level '{name}' does not exist.")
