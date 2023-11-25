import datetime
import os
import threading
from typing import Optional

from core.logger.logger_interface import IExecutionLogger


class FileLogger(IExecutionLogger):
    _lock: threading.Lock = threading.Lock()
    _base_directory: str
    _subdir_name: Optional[str]
    _filepath: str

    def __init__(self, log_directory: str = "logs", subdir_name: Optional[str] = None) -> None:
        self._subdir_name = subdir_name
        self._base_directory = (
            os.path.join(log_directory, subdir_name) if subdir_name else log_directory
        )
        self._create_log_directory()
        self._filepath = self._build_filepath()

    def _create_log_directory(self) -> None:
        if not os.path.exists(self._base_directory):
            os.makedirs(self._base_directory)

    def _build_filename(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"execution_{timestamp}"

    def _build_filepath(self) -> str:
        with self._lock:
            base_filename = self._build_filename()
            filepath = os.path.join(self._base_directory, f"{base_filename}.log")

            counter = 0
            while os.path.exists(filepath):
                counter += 1
                filepath = os.path.join(self._base_directory, f"{base_filename}_{counter}.log")

            return filepath

    def log(self, message: str) -> None:
        with open(self._filepath, "a") as file:
            file.write(f"{datetime.datetime.now().isoformat()}: {message}\n")
