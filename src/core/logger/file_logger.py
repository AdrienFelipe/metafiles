import datetime
import os
import threading
from typing import List, Optional

from core.logger.logger_interface import IExecutionLogger


class FileLogger(IExecutionLogger):
    _lock: threading.Lock = threading.Lock()
    _log_directory: str
    _name_suffix: Optional[str]
    _filepath: str

    def __init__(self, log_directory: str = "logs", name_suffix: Optional[str] = None) -> None:
        self._log_directory = log_directory
        self._name_suffix = name_suffix
        self._create_log_directory()
        self._filepath = self._build_filepath()

    def _create_log_directory(self) -> None:
        if not os.path.exists(self._log_directory):
            os.makedirs(self._log_directory)

    def _build_filename(self) -> List[str]:
        filename_parts = ["execution"]
        if self._name_suffix:
            filename_parts.append(self._name_suffix)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_parts.append(timestamp)

        return filename_parts

    def _build_filepath(self) -> str:
        with self._lock:
            base_filename_parts = self._build_filename()
            counter = 0

            while True:
                if counter > 0:
                    filename_parts = base_filename_parts + [str(counter)]
                else:
                    filename_parts = base_filename_parts

                filename = "_".join(filename_parts) + ".log"
                filepath = os.path.join(self._log_directory, filename)

                if not os.path.exists(filepath):
                    return filepath

                counter += 1

    def log(self, message: str) -> None:
        with open(self._filepath, "a") as file:
            file.write(f"{datetime.datetime.now().isoformat()}: {message}\n")
