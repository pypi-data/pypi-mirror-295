import inspect
import logging
from datetime import datetime


class TimeExecutionLogger:
    def __init__(self, with_logger, level=logging.INFO):
        self.logger = with_logger
        self.level = level
        self.start_time = datetime.now()
        caller_frame = inspect.stack()[
            2]  # Получаем информацию о вызывающем коде (2 - это индекс фрейма с вызывающим кодом)
        self.caller_file = caller_frame.filename
        self.caller_line = caller_frame.lineno
        self.logger.log(self.level,
                        f"Начало выполнения блока кода в {self.start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}. Вызвано из файла '{self.caller_file}', строка {self.caller_line}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        execution_time = (end_time - self.start_time).total_seconds()
        if exc_type is None:
            self.logger.log(self.level,
                            f"Завершение выполнения блока кода в {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}. Время выполнения: {execution_time:.6f} секунд. Вызвано из файла '{self.caller_file}', строка {self.caller_line}")
        else:
            self.logger.log(self.level,
                            f"Завершение выполнения блока кода с ошибкой {exc_val} в {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}. Время выполнения: {execution_time:.6f} секунд. Вызвано из файла '{self.caller_file}', строка {self.caller_line}")
        return False  # Возвращаем False, чтобы исключение продолжило подъём