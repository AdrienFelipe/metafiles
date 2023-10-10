from typing import Any, Callable, Dict

from agent_interface import AgentInterface
from callbacks import choose_agent_roles_callback
from openai_agent import OpenAIAgent
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

    def get_agent(self) -> AgentInterface:
        return OpenAIAgent("gpt-3.5-turbo", 1024, 0)
