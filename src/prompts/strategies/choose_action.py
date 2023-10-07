from typing import Any, Callable, Dict

from callbacks import choose_action_callback
from prompt_result import PromptResponse
from prompts.prompt_strategy import IPromptStrategy
from registry import action_registry
from task import Task


class ChooseActionStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "choose_action.yaml"
    _HANDLER_FUNCTIONS = {
        "apply_action": choose_action_callback,
    }

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "name": task.name,
            "goal": task.goal,
            "actions": action_registry.get_registered_actions(),
        }

    def handler_functions(self) -> Dict[str, Callable[[Task], PromptResponse]]:
        return self._HANDLER_FUNCTIONS
