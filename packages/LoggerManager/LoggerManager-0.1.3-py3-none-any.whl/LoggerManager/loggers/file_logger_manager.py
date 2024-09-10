import os
from typing import Sequence, Optional
import logging
import logging.handlers
from LoggerManager.loggers import BaseLoggerManager
from LoggerManager.utils import FileFormatter, MultiLevelFilter, LevelFilter, LogLevel, LoggerErrors, level_setting_decorator

class FileLoggerManager(BaseLoggerManager):
    def _create_log_directory(self, log_dir: str):
        """Создает директорию для логов, если она не существует."""
        try:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            self._internal_logger.log_info(f"Директория для логов '{log_dir}' создана или уже существует")
        except Exception as e:
            self._internal_logger.log_error(f"Ошибка при создании директории для логов: {e}")
            raise LoggerErrors(f"Ошибка при создании директории для логов: {e}")

    def _remove_existing_file_handler(self):
        """Удаляет существующий файловый обработчик, если он есть."""
        if self._file_handler:
            self._logger.removeHandler(self._file_handler)
            self._file_handler.close()
            self._internal_logger.log_info("Старый файловый обработчик удален")

    def _setup_file_handler(self, log_path: str):
        """Создает и настраивает новый файловый обработчик с ротацией логов."""
        try:
            self._file_handler = logging.handlers.RotatingFileHandler(
                log_path,
                maxBytes=self._max_bytes,
                backupCount=self._backup_count
            )
            self._file_handler.setLevel(self._logger.level)
            self._file_handler.setFormatter(self.file_formatter)
            self._logger.addHandler(self._file_handler)
            self._internal_logger.log_info(f"Логирование в файл '{log_path}' включено")
        except Exception as e:
            self._internal_logger.log_error(f"Ошибка при настройке файлового логгера с ротацией: {e}")
            raise LoggerErrors(f"Ошибка при настройке файлового логгера с ротацией: {e}")

    def __init__(self,
                 name: str,
                 level: LogLevel = "DEBUG",
                 file_format: str = None,
                 log_to_file: bool = False,
                 log_dir: str = 'logs',
                 file_name: str = 'app.log',
                 max_bytes: int = 1024 * 1024,
                 backup_count: int = 5,
                 **kwargs):
        super().__init__(name, level, **kwargs)

        self._max_bytes: int = max_bytes
        self._backup_count: int = backup_count

        self._file_handler: Optional[logging.FileHandler] = None
        self.file_formatter = FileFormatter(file_format)
        self._file_log_filter: Optional[logging.Filter] = None

        if log_to_file:
            self.enable_file_logging(file_name, log_dir)

    def enable_file_logging(self, file_name: str = 'app.log', log_dir: str = 'logs'):
        """Основная функция для включения логирования в файл."""
        self._create_log_directory(log_dir)
        self._remove_existing_file_handler()
        log_path = os.path.join(log_dir, file_name)
        self._setup_file_handler(log_path)

    def disable_file_logging(self):
        """Отключение логирования в файл"""
        if self._file_handler:
            self._logger.removeHandler(self._file_handler)
            self._file_handler.close()
            self._file_handler = None
            self._internal_logger.log_info("Логирование в файл отключено")
        else:
            self._internal_logger.log_warning(
                "Обработчик файла логирования уже отключен или не был инициализирован"
            )

    def set_file_handler_params(self, max_bytes: int, backup_count: int):
        """Установка параметров для RotatingFileHandler."""
        self._max_bytes = max_bytes
        self._backup_count = backup_count
        if self._file_handler:
            self._file_handler.maxBytes = max_bytes
            self._file_handler.backupCount = backup_count
            self._internal_logger.log_info(
                f"Изменены параметры RotatingFileHandler: maxBytes={max_bytes}, backupCount={backup_count}"
            )
        else:
            self._internal_logger.log_warning(
                "Файловый обработчик не инициализирован. Новые параметры будут применены при следующем включении логирования в файл."
            )

    @level_setting_decorator
    def set_file_level(self, level: LogLevel):
        """Устанавливает уровень логирования для файлового обработчика"""
        if self._file_handler:
            self._file_handler.setLevel(level)
            self._internal_logger.log_info(f"Уровень логирования для файлового обработчика установлен на {level}")
        else:
            self._internal_logger.log_warning("Файловый обработчик не был инициализирован")

    def reset_file_level(self):
        """Сброс уровня логирования для файлового обработчика на DEBUG"""
        self.set_file_level('DEBUG')

    def set_file_filter(self, level: LogLevel):
        """Установка фильтра для логирования только на файловый обработчик"""
        log_level = self._LEVEL_MAPPING.get(level)
        if log_level is not None:
            self.clear_file_filter()
            if self._file_handler:
                self._file_handler.addFilter(LevelFilter(log_level))
            self._internal_logger.log_info(f"Фильтр уровня логирования установлен на {level} для файлового обработчика")
        else:
            self._internal_logger.log_error(
                f"Некорректный уровень фильтра: {level}. Используйте один из: {list(self._LEVEL_MAPPING.keys())}"
            )

    def set_file_filter_list(self, levels: Sequence[LogLevel]):
        """Установка списка фильтров для логирования только на файловый обработчик"""
        valid_levels = self._validate_and_map_levels(levels)
        if valid_levels is None:
            return

        self.clear_file_filter()
        if self._file_handler:
            self._file_log_filter = MultiLevelFilter(valid_levels)
            self._file_handler.addFilter(self._file_log_filter)
            self._internal_logger.log_info(
                f"Фильтр уровней логирования установлен на {levels} для файлового обработчика")
        else:
            self._internal_logger.log_warning("Файловый обработчик не был инициализирован")

    def clear_file_filter(self):
        """Очистка установленного фильтра для файлового обработчика"""
        if self._file_handler and self._file_handler.filters:
            self._file_handler.filters.clear()
            self._internal_logger.log_info("Фильтр логирования для файлового обработчика очищен")
        else:
            self._internal_logger.log_warning("Файловый обработчик не имеет фильтров или не был инициализирован")

    def set_file_format(self, format_string: str):
        """Устанавливает формат для файлового логирования."""
        self.file_formatter.set_format(format_string)
        self._internal_logger.log_info(
            f"Установлен формат для файлового логирования: {format_string }"
        )

    def set_file_level_format(self, level: LogLevel, format_string: str):
        """Устанавливает формат для файлового логирования."""
        self.file_formatter.set_level_format(level, format_string)
        self._internal_logger.log_info(
            f"Установлен формат для файлового логирования: {level + ' - ' + format_string}"
        )

