from typing import Any, Callable, Dict, Optional
from callbacks import execute_action
from task import Task
from prompts.prompt_strategy import IPromptStrategy
from registry import action_registry


class ChooseActionStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "choose_action.yaml"
    _HANDLER_FUNCTIONS = {
        "apply_action": execute_action,
    }

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "name": task.name,
            "goal": task.goal,
            "actions": action_registry.get_registered_actions(),
        }

    def get_handler_function(self, function_name: str) -> Optional[Callable]:
        return self._HANDLER_FUNCTIONS.get(function_name)
