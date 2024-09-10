from typing import Sequence
from LoggerManager.utils import TimeExecutionLogger, LogLevel
from LoggerManager.loggers import ConsoleLoggerManager, FileLoggerManager


class LoggerManager(ConsoleLoggerManager, FileLoggerManager):
    def __init__(self,
                 *,
                 name: str,
                 level: LogLevel = "DEBUG",
                 console_format: str = None,
                 file_format: str = None,
                 log_to_file: bool = False,
                 log_dir: str = 'logs',
                 file_name: str = 'app.log',
                 max_bytes: int = 1024 * 1024,
                 backup_count: int = 5):
        kwargs = {"name": name,
                 "level": level,
                 "console_format": console_format,
                 "file_format": file_format,
                 "log_to_file": log_to_file,
                 "log_dir": log_dir,
                 "file_name": file_name,
                 "max_bytes": max_bytes,
                 "backup_count": backup_count}
        super().__init__(**kwargs)

    def set_all_level(self, level: LogLevel):
        """Установка уровня логирования"""
        log_level = self._LEVEL_MAPPING.get(level)
        if log_level is not None:
            self._logger.setLevel(log_level)
            if self._console_handler:
                self._console_handler.setLevel(log_level)
            if self._file_handler:
                self._file_handler.setLevel(log_level)
            self._internal_logger.log_info(f"Уровень логирования глобально установлен на {level}")
        else:
            self._internal_logger.log_error(
                f"Некорректный уровень логирования: {level}. Используйте один из: {list(self._LEVEL_MAPPING.keys())}"
            )

    def reset_all_level(self):
        """Сброс уровня логирования до уровня DEBUG"""
        self.set_all_level('DEBUG')

    def set_all_filter(self, level: LogLevel):
        """Установка фильтра для логирования глобально"""
        log_level = self._LEVEL_MAPPING.get(level)
        if log_level is not None:
            self.set_filter(level)
            self.set_console_filter(level)
            self.set_file_filter(level)
        else:
            self._internal_logger.log_error(
                f"Некорректный уровень фильтра: {level}. Используйте один из: {list(self._LEVEL_MAPPING.keys())}"
            )

    def set_all_filter_list(self, levels: Sequence[LogLevel]):
        """Установка списка фильтров для логирования глобально"""
        valid_levels = self._validate_and_map_levels(levels)
        if valid_levels is None:
            return
        self.set_filter_list(levels)
        self.set_console_filter_list(levels)
        self.set_file_filter_list(levels)

    def clear_all_filter(self):
        """Удаление всех фильтров глобально"""
        self.clear_filter()
        self.clear_file_filter()
        self.clear_console_filter()

    def time_execution(self):
        """Контекстный менеджер для логирования времени выполнения блока кода"""
        return TimeExecutionLogger(self._internal_logger.logger)