import logging
from typing import Sequence


class MultiLevelFilter(logging.Filter):
    def __init__(self, levels: Sequence[int]):
        super().__init__()
        self.levels = levels

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno in self.levels

class LevelFilter(logging.Filter):
    def __init__(self, level: int):
        super().__init__()
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.level