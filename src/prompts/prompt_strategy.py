from abc import ABC, abstractmethod
from typing import Any, Callable, Dict

from agent_interface import AgentInterface
from prompt_result import PromptResponse
from task import Task


class IPromptStrategy(ABC):
    @abstractmethod
    def get_template_name(self) -> str:
        pass

    @abstractmethod
    def get_render_args(self, task: Task) -> Dict[str, Any]:
        pass

    @abstractmethod
    def handler_functions(self) -> Dict[str, Callable[[Task], PromptResponse]]:
        pass

    @abstractmethod
    def get_agent(self) -> AgentInterface:
        pass
