from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional
from task import Task


class IPromptStrategy(ABC):
    @abstractmethod
    def get_template_name(self) -> str:
        pass

    @abstractmethod
    def get_render_args(self, task: Task) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_handler_function(self, function_name: str) -> Optional[Callable]:
        """
        This method should return the actual function to be executed based on the function name.
        If the function_name is not found, it should return None.
        It will be implemented by concrete strategies.
        """
        pass
