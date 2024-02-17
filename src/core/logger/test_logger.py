import os

from core.logger.file_logger import FileLogger
from core.service.service_container import ServiceContainer


class TestLogger(FileLogger):
    def __init__(self, container: ServiceContainer, name_suffix: str) -> None:
        path = os.path.join("logs", "test")
        super().__init__(container, path, name_suffix)
