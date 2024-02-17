import datetime
import os
import threading
from typing import Dict, Optional

import yaml

from core.logger.logger_interface import IExecutionLogger
from core.service.service_container import ServiceContainer
from prompt.prompt_result import PromptStatus
from task.task import Task


# Make yaml logs smart multiline
def smart_string_presenter(dumper, data):
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


# For yaml logs to be human readable
def enum_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data.name)


def task_representer(dumper, task: Task):
    return dumper.represent_scalar("tag:yaml.org,2002:str", f"[{task.id}] {task.goal}")


yaml.add_representer(str, smart_string_presenter)
yaml.add_representer(PromptStatus, enum_representer)
yaml.add_representer(Task, task_representer)


class FileLogger(IExecutionLogger):
    _lock: threading.Lock = threading.Lock()
    _base_directory: str
    _filepath: str

    def __init__(
        self,
        container: ServiceContainer,
        log_directory: str = "logs",
        subdir_name: Optional[str] = None,
    ) -> None:
        super().__init__(container=container)
        self._base_directory = (
            os.path.join(log_directory, subdir_name) if subdir_name else log_directory
        )
        self._create_log_directory()
        self._filepath = self._build_filepath()

    def add_subdir(self, subdir_name: str) -> None:
        self._base_directory = os.path.join(self._base_directory, subdir_name)

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

    def log(self, message: str, data: Optional[Dict] = None) -> None:
        with open(self._filepath, "a") as file:
            file.write(f"{datetime.datetime.now().isoformat()}: {message}\n")
            if data:
                file.write(yaml.dump(data, sort_keys=False, width=999))
