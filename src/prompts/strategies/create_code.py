from typing import Any, Callable, Dict

from agent_config import AgentConfig, ModelType
from callbacks import create_code_callback
from prompt_result import PromptResponse
from prompts.prompt_strategy import IPromptStrategy
from task import Task


class CreateCodeStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "create_code.yaml"
    _HANDLER_FUNCTIONS = {
        "execute_code": create_code_callback,
    }

    def __init__(self, agent_role: str) -> None:
        super().__init__()
        self.agent_role = agent_role

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "role": self.agent_role,
            "task": task.goal,
            "goal": task.requirements,
            "plan": task.plan,
        }

    def handler_functions(self) -> Dict[str, Callable[[Task], PromptResponse]]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.CAPABLE, 4096, 0)
