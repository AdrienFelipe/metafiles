from typing import Any, Callable, Dict

from agent.agent_config import AgentConfig, ModelType
from prompt.callbacks.choose_agent import choose_agent_roles_callback
from prompt.prompt_strategy import IPromptStrategy
from task.task import Task


class ChooseAgentStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "choose_agent.yaml"
    _HANDLER_FUNCTIONS: Dict[str, Callable] = {
        "ask_agents": choose_agent_roles_callback,
    }

    def __init__(self, reason: str = "") -> None:
        super().__init__()
        self._reason = reason

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "goal": task.goal,
            "definition": task.definition,
            "specifics": task.specifics,
            "reason": self._reason,
        }

    def callbacks(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.FAST, 1024, 0)
