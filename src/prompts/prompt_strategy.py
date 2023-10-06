from abc import ABC, abstractmethod
from typing import Any, Dict
from task import Task

class IPromptStrategy(ABC):
    
    @abstractmethod
    def get_template_name(self) -> str:
        pass
    
    @abstractmethod
    def get_render_args(self, task: Task) -> Dict[str, Any]:
        pass
