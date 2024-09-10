from typing import Sequence, Optional
import logging
import logging.handlers
from LoggerManager.loggers import BaseLoggerManager
from LoggerManager.utils import ConsoleFormatter, MultiLevelFilter, LevelFilter, LogLevel, ColorName, level_setting_decorator


class ConsoleLoggerManager(BaseLoggerManager):
    def _setup_console_handler(self, level: LogLevel):
        """Настройка консольного обработчика и форматтера"""
        log_level = self._LEVEL_MAPPING.get(level)
        if log_level is not None:
            self._console_handler = logging.StreamHandler()
            self._console_handler.setLevel(log_level)
            self._console_handler.setFormatter(self._console_formatter)
            self._logger.addHandler(self._console_handler)
        else:
            self._internal_logger.log_error(
                f"Некорректный уровень логирования: {level}. Используйте один из: {list(self._LEVEL_MAPPING.keys())}"
            )

    def __init__(self,
                 name: str,
                 level: LogLevel = "DEBUG",
                 console_format: str = None,
                 **kwargs):
        super().__init__(name, level, **kwargs)

        self._console_handler: Optional[logging.StreamHandler] = None
        self._console_formatter = ConsoleFormatter(console_format)
        self._console_log_filter: Optional[logging.Filter] = None

        self._setup_console_handler(level)

    @level_setting_decorator
    def set_console_level(self, level: LogLevel):
        """Устанавливает уровень логирования для консольного обработчика"""
        if self._console_handler:
            self._console_handler.setLevel(level)
            self._internal_logger.log_info(f"Уровень логирования для консольного обработчика установлен на {level}")
        else:
            self._internal_logger.log_warning("Консольный обработчик не был инициализирован")

    def reset_console_level(self):
        """Сброс уровня логирования для консольного обработчика на DEBUG"""
        self.set_console_level('DEBUG')

    def set_console_filter(self, level: LogLevel):
        """Установка фильтра для логирования только на консольный обработчик"""
        log_level = self._LEVEL_MAPPING.get(level)
        if log_level is not None:
            self.clear_filter()
            if self._console_handler:
                self._console_handler.addFilter(LevelFilter(log_level))
            self._internal_logger.log_info(
                f"Фильтр уровня логирования установлен на {level} для консольного обработчика")
        else:
            self._internal_logger.log_error(
                f"Некорректный уровень фильтра: {level}. Используйте один из: {list(self._LEVEL_MAPPING.keys())}"
            )

    def set_console_filter_list(self, levels: Sequence[LogLevel]):
        """Установка списка фильтров для логирования только на консольный обработчик"""
        valid_levels = self._validate_and_map_levels(levels)
        if valid_levels is None:
            return

        self.clear_console_filter()
        if self._console_handler:
            self._console_log_filter = MultiLevelFilter(valid_levels)
            self._console_handler.addFilter(self._console_log_filter )
            self._internal_logger.log_info(
                f"Фильтр уровней логирования установлен на {levels} для консольного обработчика")
        else:
            self._internal_logger.log_warning("Консольный обработчик не был инициализирован")

    def clear_console_filter(self):
        """Очистка установленного фильтра для консольного обработчика"""
        if self._console_handler and self._console_handler.filters:
            self._console_handler.filters.clear()
            self._internal_logger.log_info("Фильтр логирования для консольного обработчика очищен")
        else:
            self._internal_logger.log_warning("Консольный обработчик не имеет фильтров или не был инициализирован")

    def set_console_format(self, format_string: str):
        """Устанавливает формат для консольного логирования."""
        self._console_formatter.set_format(format_string)
        self._internal_logger.log_info(
            f"Установлен формат для консольного логирования: {format_string}"
        )

    def set_console_level_format(self, level: LogLevel, format_string: str):
        """Устанавливает формат для консольного логирования."""
        self._console_formatter.set_level_format(level, format_string)
        self._internal_logger.log_info(
            f"Установлен формат для консольного логирования: {level+' '+format_string}"
        )

    def set_console_color(self, level: LogLevel, color: ColorName):
        """Устанавливает цвет для консольного логирования."""
        self._console_formatter.set_color(level, color)
        self._internal_logger.log_info(
            f"Установлен цвет - {color}; для консольного логирования - {level}"
        )

    def enable_console_logging(self):
        """Включение логирования в консоль"""
        if self._console_handler:
            self._console_handler.setLevel(self._logger.level)
            self._internal_logger.log_info("Логирование в консоль включено")

    def disable_console_logging(self):
        """Отключение логирования в консоль"""
        if self._console_handler:
            self._console_handler.setLevel(logging.CRITICAL + 1)
            self._internal_logger.log_info("Логирование в консоль отключено")
        else:
            self._internal_logger.log_warning(
                "Обработчик консольного логирования уже отключен или не был инициализирован")