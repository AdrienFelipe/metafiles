import os

from core.logger.file_logger import FileLogger


class TestLogger(FileLogger):
    def __init__(self, name_suffix: str) -> None:
        path = os.path.join("logs", "test")
        super().__init__(path, name_suffix)
