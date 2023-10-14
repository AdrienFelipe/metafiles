from typing import Any, Callable, Dict

from action_registry import action_registry
from agent_config import AgentConfig, ModelType
from callbacks import choose_action_callback
from prompts.prompt_strategy import IPromptStrategy
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
            "name": task.goal,
            "goal": task.requirements,
            "actions": action_registry.get_registered_actions(),
        }

    def handler_functions(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.FAST, 512, 0)
