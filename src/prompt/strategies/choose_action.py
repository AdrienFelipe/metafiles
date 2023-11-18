from typing import Any, Callable, Dict

from action.action_registry import action_registry
from agent.agent_config import AgentConfig, ModelType
from prompt.callbacks.choose_action import choose_action_callback
from prompt.prompt_strategy import IPromptStrategy
from task.task import Task


class ChooseActionStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "choose_action.yaml"
    _HANDLER_FUNCTIONS = {
        "apply_action": choose_action_callback,
    }

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "goal": task.goal,
            "definition": task.definition,
            "specifics": task.specifics,
            "actions": action_registry.get_registered_actions(),
        }

    def callbacks(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.FAST, 512, 0)
