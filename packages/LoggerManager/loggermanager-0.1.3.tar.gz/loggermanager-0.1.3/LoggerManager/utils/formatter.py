import logging
from LoggerManager.utils import LogLevel, ColorName


class BaseFormatter(logging.Formatter):
    DEFAULT_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    #DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    def __init__(self, default_format=None):
        super().__init__()
        self.default_format = default_format or self.DEFAULT_FORMAT
        self.formats = {}

    def set_format(self, format_string: str ):
        self._save_format(format_string)

    def set_level_format(self, level: LogLevel, format_string: str):
        """Устанавливает форматирование для заданного уровня логирования."""
        log_level = getattr(logging, level.upper(), None)
        if log_level is not None:
            self._save_level_format(log_level, format_string)
        else:
            raise ValueError(f"Некорректный уровень логирования: {level}")

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.formats.get(record.levelno, self.default_format)
        self._style._fmt = log_fmt
        return super().format(record)

    def _save_format(self, format_string: str):
        self.formats = {
            level: format_string
            for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        }

    def _save_level_format(self, log_level: int, format_string: str):
        self.formats[log_level] = format_string


class ConsoleFormatter(BaseFormatter):
    COLORS = {
        "black": "\x1b[30m",
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "magenta": "\x1b[35m",
        "cyan": "\x1b[36m",
        "white": "\x1b[37m",
        "reset": "\x1b[0m"
    }

    def __init__(self, default_format=None):
        super().__init__(default_format)
        self.level_colors = {
            logging.DEBUG: self.COLORS["green"],
            logging.INFO: self.COLORS["magenta"],
            logging.WARNING: self.COLORS["yellow"],
            logging.ERROR: self.COLORS["blue"],
            logging.CRITICAL: self.COLORS["cyan"]
        }
        self.formats = {
            level: color + self.default_format + self.COLORS["reset"]
            for level, color in self.level_colors.items()
        }

    def set_color(self, level: LogLevel, color: ColorName):
        """Устанавливает цвет для заданного уровня логирования."""
        log_level = getattr(logging, level.upper(), None)
        if log_level in self.level_colors:
            self.level_colors[log_level] = self.COLORS[color]
            self.formats[log_level] = self.level_colors[log_level] + self.default_format + self.COLORS["reset"]
        else:
            raise ValueError(f"Некорректный уровень логирования: {level}")

    def _save_format(self, format_string: str):
        self.formats = {
            level: self.level_colors[level] + format_string + self.COLORS["reset"]
            for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        }

    def _save_level_format(self, log_level: int, format_string: str):
        self.formats[log_level] = self.level_colors[log_level] + format_string + self.COLORS["reset"]


class FileFormatter(BaseFormatter):
    def __init__(self, default_format=None):
        super().__init__(default_format)
        # Форматы для файлового вывода по умолчанию те же, что и базовый формат
        self.formats = {
            level: self.default_format
            for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        }