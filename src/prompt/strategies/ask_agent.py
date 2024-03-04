from typing import Any, Callable, Dict, List

from agent.agent_config import AgentConfig, ModelType
from prompt.callbacks.ask_code import ask_for_code_callback
from prompt.callbacks.query_user import query_user_callback
from prompt.callbacks.task import add_task_depedencies_callback, execute_task_callback
from prompt.callbacks.validate_response import validate_response_callback
from prompt.prompt_strategy import IPromptStrategy
from task.task import Task
from task.task_predecessor_finder import TaskPredecessorFinder


class AskAgentStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "ask_agent.yaml"
    _HANDLER_FUNCTIONS: Dict[str, Callable] = {
        "ask_user": query_user_callback,
        "add_dependency": add_task_depedencies_callback,
        "execute_task": execute_task_callback,
        "escalate_to_code": ask_for_code_callback,
        "approve_response": validate_response_callback,
    }

    def __init__(self) -> None:
        super().__init__()
        self.role: str = ""
        self.dependencies: List[Task] = []
        self.messages: List[str] = []

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "task_id": task.id,
            "goal": task.goal,
            "definition": task.definition,
            "specifics": task.specifics,
            "response": task.response,
            "dependencies_tasks": task.depends_on,
            "role": self.role,
            "messages": self.messages,
            "predecessor_tasks": TaskPredecessorFinder.generate(task),
            "queries": task.queries,
        }

    def set_role(self, role: str) -> None:
        self.role = role

    def add_message(self, message: str) -> None:
        self.messages.append(message)

    def callbacks(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.FAST, 1024, 0)
