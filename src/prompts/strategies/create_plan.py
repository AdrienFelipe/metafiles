from typing import Any, Callable, Dict

from agent_interface import AgentInterface
from callbacks import create_plan_parse_callback, query_user_callback, validate_plan_callback
from openai_agent import OpenAIAgent
from prompt_result import PromptResponse
from prompts.prompt_strategy import IPromptStrategy
from task import Task


class CreatePlanStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "create_plan.yaml"
    _HANDLER_FUNCTIONS = {
        "update_plan": create_plan_parse_callback,
        "validate_plan": validate_plan_callback,
        "ask_user": query_user_callback,
    }

    def __init__(self, agent_role: str) -> None:
        super().__init__()
        self.agent_role = agent_role

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "role": self.agent_role,
            "task": task.goal,
            "goal": task.requirements,
            "plan": task.plan,
        }

    def handler_functions(self) -> Dict[str, Callable[[Task], PromptResponse]]:
        return self._HANDLER_FUNCTIONS

    def get_agent(self) -> AgentInterface:
        return OpenAIAgent("gpt-3.5-turbo", 2048, 0)
