from typing import Any, Callable, Dict

from agent.agent_config import AgentConfig, ModelType
from prompt.callbacks.code import create_code_callback, validate_code_callback
from prompt.callbacks.query_user import query_user_callback
from prompt.callbacks.task import (
    divide_task_callback,
    execute_task_callback,
    get_tasks_results_callback,
)
from prompt.prompt_strategy import IPromptStrategy
from task import Task


class CreateCodeStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "create_code.yaml"
    _HANDLER_FUNCTIONS: Dict[str, Callable] = {
        "execute_code": create_code_callback,
        "validate_code": validate_code_callback,
        "ask_user": query_user_callback,
        "divide_task": divide_task_callback,
        "execute_task": execute_task_callback,
        "tasks_results": get_tasks_results_callback,
    }

    def __init__(self, agent_role: str) -> None:
        super().__init__()
        self.agent_role = agent_role

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "task_id": task.id,
            "task": task.goal,
            "requirements": task.requirements,
            "code": task.plan,
            "tasks": task.get_parent_tasks(),
            "clarifications": ["question1", "question2", "question3"],
            "issues": ["issue1", "issue2", "issue3"],
        }

    def handler_functions(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.CAPABLE, 4096, 0)
