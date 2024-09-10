import logging


class InternalLogger:
    def __init__(self, name: str = "InternalLogger"):
        """Инициализация внутреннего логгера."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.DEBUG)
        self.handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"))
        self.logger.addHandler(self.handler)

    @property
    def name(self) -> str:
        """Возвращает имя логгера."""
        return self.logger.name

    @name.setter
    def name(self, new_name: str):
        """Устанавливает новое имя логгера."""
        self.logger.name = new_name

    def log_info(self, message: str):
        """Логирование информационного сообщения."""
        self.logger.info(message)

    def log_warning(self, message: str):
        """Логирование информационного сообщения."""
        self.logger.warning(message)

    def log_error(self, message: str):
        """Логирование сообщения об ошибке."""
        self.logger.error(message)

    def enable_logging(self):
        """Включение логирования."""
        self.handler.setLevel(logging.DEBUG)
        self.log_info("Внутреннее логирование включено")

    def disable_logging(self):
        """Отключение логирования."""
        self.log_info("Внутреннее логирование отключено")
        self.handler.setLevel(logging.CRITICAL + 1)

