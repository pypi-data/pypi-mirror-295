from functools import wraps
from LoggerManager.utils import LogLevel


def level_setting_decorator(func):
    @wraps(func)
    def wrapper(self, level: LogLevel):
        log_level = self._LEVEL_MAPPING.get(level)
        if log_level is not None:
            func(self, log_level)  # Вызываем оригинальную функцию с установленным log_level
        else:
            self._internal_logger.log_error(
                f"Некорректный уровень логирования: {level}. Используйте один из: {list(self._LEVEL_MAPPING.keys())}"
            )
    return wrapper