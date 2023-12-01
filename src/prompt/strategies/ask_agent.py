from typing import Any, Callable, Dict, List

from agent.agent_config import AgentConfig, ModelType
from prompt.callbacks.ask_code import ask_for_code_callback
from prompt.callbacks.query_user import query_user_callback
from prompt.callbacks.task import execute_task_callback, get_tasks_results_callback
from prompt.prompt_strategy import IPromptStrategy
from prompt.strategies.create_code import Query
from task.task import Task


class AskAgentStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "ask_agent.yaml"
    _HANDLER_FUNCTIONS: Dict[str, Callable] = {
        "ask_user": query_user_callback,
        "tasks_results": get_tasks_results_callback,
        "execute_task": execute_task_callback,
        "escalate_to_code": ask_for_code_callback,
    }

    def __init__(self) -> None:
        super().__init__()
        self.role: str = ""
        self.queries: List[Query] = []
        self.dependencies: List[Task] = []

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "goal": task.goal,
            "definition": task.definition,
            "specifics": task.specifics,
            "response": task.response,
            "role": self.role,
            "sibling_tasks": task.get_siblings_by_position(),
            "queries": self.queries,
            "dependencies_tasks": self.dependencies,
        }

    def set_role(self, role: str) -> None:
        self.role = role

    def add_query(self, question: str, answer: str) -> None:
        self.queries.append(Query(question, answer))

    def add_dependencies(self, tasks: List[Task]) -> None:
        self.dependencies.extend(tasks)

    def callbacks(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.FAST, 1024, 0)
