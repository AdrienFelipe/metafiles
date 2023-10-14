from typing import Any, Callable, Dict

from agent_config import AgentConfig, ModelType
from callbacks import choose_agent_roles_callback
from prompt_result import PromptResponse
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
        return {"name": task.goal, "goal": task.requirements}

    def handler_functions(self) -> Dict[str, Callable[[Task], PromptResponse]]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.FAST, 1024, 0)
