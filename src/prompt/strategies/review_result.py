from typing import Any, Callable, Dict, List

from agent.agent_config import AgentConfig, ModelType
from prompt.callbacks.review_result import approve_result_callback, reject_result_callback
from prompt.prompt_strategy import IPromptStrategy
from task.task import Task


class ReviewResultStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "review_result.yaml"
    _HANDLER_FUNCTIONS: Dict[str, Callable] = {
        "approve_result": approve_result_callback,
        "reject_result": reject_result_callback,
    }

    def __init__(self) -> None:
        super().__init__()
        self.messages: List[str] = []

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "goal": task.goal,
            "definition": task.definition,
            "specifics": task.specifics,
            "result": task.result.message if task.result else "",
            "messages": self.messages,
        }

    def callbacks(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.FAST, 2048, 0)

    def add_message(self, message: str) -> None:
        self.messages.append(message)
