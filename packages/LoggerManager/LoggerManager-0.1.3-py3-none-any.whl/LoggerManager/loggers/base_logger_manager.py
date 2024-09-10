import os
import platform
from typing import Sequence, Optional
import logging
import logging.handlers
from LoggerManager.utils import MultiLevelFilter, LevelFilter, LogLevel, InternalLogger


# Дополнительная проверка для ОС Windows
if platform.system() == "Windows":
    os.system('color')

class BaseLoggerManager:
    _LEVEL_MAPPING = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    @staticmethod
    def _check_logger_name(name: str) -> tuple[str, Optional[str]]:
        if not isinstance(name, str) or not name.strip():
            # Устанавливаем имя по умолчанию и формируем предупреждение
            default_name = "DefaultLogger"
            warning_message = f"Некорректное имя логгера: '{name}'. Устанавливается имя по умолчанию '{default_name}'."
            return default_name, warning_message
        return name, None

    def _validate_and_map_levels(self, levels: Sequence[LogLevel]) -> Optional[list[int]]:
        """Проверка списка уровней и их преобразование в соответствующие значения из _LEVEL_MAPPING"""
        if not levels:
            self._internal_logger.log_error("Список уровней фильтра не должен быть пустым.")
            return None

        valid_levels = [self._LEVEL_MAPPING[level] for level in levels if level in self._LEVEL_MAPPING]

        if not valid_levels:
            self._internal_logger.log_error(
                f"Некорректные уровни фильтра: {levels}. Используйте один из: {list(self._LEVEL_MAPPING.keys())}"
            )
            return None
        return valid_levels

    def _create_logger(self) -> logging.Logger:
        """Можно переопределить фабричный метод для инициализации собственного логгера"""
        return logging.getLogger(self.name)

    def __init__(self,
                 name: str,
                 level: LogLevel = "DEBUG",
                 **kwargs):

        # Проверка имени логгера и установка корректного имени
        self.name, name_warning = self._check_logger_name(name)

        self._internal_logger = InternalLogger(name=f"{self.name}_internal")
        if name_warning:
            self._internal_logger.log_warning(name_warning)

        # Основной логгер
        self._logger = self._create_logger()
        self._logger.setLevel(level)
        self._log_filter: Optional[logging.Filter] = None

    @property
    def logger(self) -> logging.Logger:
        """Свойство для доступа к приватному логгеру."""
        return self._logger

    def set_name(self, name: str):
        """Установка нового имени логгера"""
        if not isinstance(name, str) or not name.strip():
            self._internal_logger.log_error(f"Некорректное новое имя логгера: '{name}'. Имя остается без изменений.")
            return

        self._logger.name = name
        self._internal_logger.name = f"{name}_internal"
        self._internal_logger.log_info(f"Имя логгера изменено на '{name}'")

    def set_filter(self, level: LogLevel):
        """Установка фильтра для логирования"""
        log_level = self._LEVEL_MAPPING.get(level)
        if log_level is not None:
            self.clear_filter()
            self._log_filter = LevelFilter(log_level)
            self._logger.addFilter(self._log_filter)
            self._internal_logger.log_info(f"Базовый фильтр уровня логирования установлен на {level}")
        else:
            self._internal_logger.log_error(
                f"Некорректный уровень фильтра: {level}. Используйте один из: {list(self._LEVEL_MAPPING.keys())}"
            )

    def set_filter_list(self, levels: Sequence[LogLevel]):
        """Установка списка фильтров для логирования"""
        valid_levels = self._validate_and_map_levels(levels)
        if valid_levels is None:
            return

        self.clear_filter()
        self._log_filter = MultiLevelFilter(valid_levels)
        self._logger.addFilter(self._log_filter)
        self._internal_logger.log_info(f"Базовый фильтр логирования уровней установлен на {levels}")
        
    def clear_filter(self):
        """Очистка установленного фильтра"""
        if self._log_filter:
            self._logger.removeFilter(self._log_filter)
            self._log_filter = None
            self._internal_logger.log_info("Базовый фильтр логирования очищен")

    def clear_level(self):
        """Сброс базового обработчика на DEBUG"""
        self._logger.setLevel('DEBUG')
        self._internal_logger.log_info(f"Уровень базового логирования установлен на DEBUG")

    # Управление внутренним логгером
    def enable_internal_logging(self):
        """Включение внутреннего логирования"""
        self._internal_logger.enable_logging()

    def disable_internal_logging(self):
        """Отключение внутреннего логирования"""
        self._internal_logger.disable_logging()

    # Управление логгером
    def enable_logging(self):
        """Включение логирования"""
        self._logger.disabled = False
        self._internal_logger.log_info("Логирование включено")

    def disable_logging(self):
        """Отключение логирования"""
        self._logger.disabled = True
        self._internal_logger.log_info("Логирование отключено")