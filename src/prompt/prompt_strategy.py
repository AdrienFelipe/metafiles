from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, TypeVar

from agent.agent_config import AgentConfig
from task.task import Task


class IPromptStrategy(ABC):
    @abstractmethod
    def get_template_name(self) -> str:
        pass

    @abstractmethod
    def get_render_args(self, task: Task) -> Dict[str, Any]:
        pass

    @abstractmethod
    def callbacks(self) -> Dict[str, Callable]:
        pass

    @abstractmethod
    def agent_config(self) -> AgentConfig:
        pass


TStrategy = TypeVar("TStrategy", bound=IPromptStrategy)
