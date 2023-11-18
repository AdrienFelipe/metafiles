from typing import Any, Callable, Dict, List, NamedTuple

from agent.agent_config import AgentConfig, ModelType
from prompt.callbacks.code import create_code_callback, validate_code_callback
from prompt.callbacks.query_user import query_user_callback
from prompt.callbacks.task import (
    divide_task_callback,
    execute_task_callback,
    get_tasks_results_callback,
)
from prompt.prompt_strategy import IPromptStrategy
from task.task import Task


class CreateCodeStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "create_code.yaml"
    _HANDLER_FUNCTIONS: Dict[str, Callable] = {
        "ask_user": query_user_callback,
        "tasks_results": get_tasks_results_callback,
        "execute_task": execute_task_callback,
        "divide_task": divide_task_callback,
        "execute_code": create_code_callback,
        "validate_code": validate_code_callback,
    }

    def __init__(self) -> None:
        super().__init__()
        self.reason: str = ""
        self.queries: List[Query] = []
        self.dependencies: List[Task] = []
        self.execution_results: List[str] = []
        self.messages: List[str] = []

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "task_id": task.id,
            "goal": task.goal,
            "requirements": task.definition,
            "code": "\n\n".join(task.plan),
            "sibling_tasks": task.get_siblings(),
            "user_queries": self.queries,
            "dependencies_tasks": self.dependencies,
            "execution_results": self.execution_results,
            "messages": self.messages,
        }

    def handler_functions(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.CAPABLE, 4096, 0)

    def set_reason(self, reason: str) -> None:
        self.reason = reason

    def add_query(self, question: str, answer: str) -> None:
        self.queries.append(Query(question, answer))

    def add_dependencies(self, tasks: List[Task]) -> None:
        self.dependencies.extend(tasks)

    def add_message(self, message: str) -> None:
        self.messages.append(message)

    def add_execution_result(self, result: str) -> None:
        self.execution_results.append(result)


class Query(NamedTuple):
    question: str
    answer: str
