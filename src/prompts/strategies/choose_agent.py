from typing import Any, Callable, Dict

from callbacks import choose_agent_roles_callback
from prompt_result import PromptResult
from prompts.prompt_strategy import IPromptStrategy
from task import Task


class ChooseAgentStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "choose_agent.yaml"
    _HANDLER_FUNCTIONS = {
        "ask_agents": choose_agent_roles_callback,
    }

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {"name": task.name, "goal": task.goal}

    def handler_functions(self) -> Dict[str, Callable[[Task], PromptResult]]:
        return self._HANDLER_FUNCTIONS
