from typing import Any, Callable, Dict

from agent.agent_config import AgentConfig, ModelType
from prompt.prompt_strategy import IPromptStrategy
from task.task import Task


class FilterRequirementsStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "filter_requirements.yaml"
    _HANDLER_FUNCTIONS: Dict[str, Callable] = {}

    def __init__(self, sub_goal: str) -> None:
        super().__init__()
        self.sub_goal = sub_goal

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "task": task.goal,
            "plan": task.plan,
            "requirements": task.definition,
            "subtask": self.sub_goal,
        }

    def callbacks(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.FAST, 2048, 0)
