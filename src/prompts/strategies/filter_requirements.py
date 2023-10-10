from typing import Any, Callable, Dict

from agent_interface import AgentInterface
from openai_agent import OpenAIAgent
from prompt_result import PromptResponse
from prompts.prompt_strategy import IPromptStrategy
from task import Task


class FilterRequirementsStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "filter_requirements.yaml"
    _HANDLER_FUNCTIONS = {}

    def __init__(self, sub_goal: str) -> None:
        super().__init__()
        self.sub_goal = sub_goal

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "task": task.goal,
            "plan": task.plan,
            "requirements": task.requirements,
            "subtask": self.sub_goal,
        }

    def handler_functions(self) -> Dict[str, Callable[[Task], PromptResponse]]:
        return self._HANDLER_FUNCTIONS

    def get_agent(self) -> AgentInterface:
        return OpenAIAgent("gpt-3.5-turbo", 2048, 0)
