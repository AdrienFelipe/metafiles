from typing import Any, Dict
from task import Task
from prompts.prompt_strategy import IPromptStrategy
from registry import action_registry


class ChooseActionStrategy(IPromptStrategy):
    TEMPLATE_NAME = "choose_action.yaml"

    def get_template_name(self) -> str:
        return self.TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "name": task.name,
            "goal": task.goal,
            "actions": action_registry.get_registered_actions(),
        }
