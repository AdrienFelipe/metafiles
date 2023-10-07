from typing import Any, Callable, Dict

from callbacks import create_plan_parse_callback, query_user_callback
from prompt_result import PromptResult
from prompts.prompt_strategy import IPromptStrategy
from task import Task


class CreatePlanStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "create_plan/create_plan.v2.yaml"
    _HANDLER_FUNCTIONS = {
        "update_plan": create_plan_parse_callback,
        "ask_user": query_user_callback,
    }

    def __init__(self, agent_role: str) -> None:
        super().__init__()
        self.agent_role = agent_role

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {"name": task.name, "goal": task.goal, "role": self.agent_role}

    def handler_functions(self) -> Dict[str, Callable[[Task], PromptResult]]:
        return self._HANDLER_FUNCTIONS