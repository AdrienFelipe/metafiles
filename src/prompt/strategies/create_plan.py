from typing import Any, Callable, Dict

from agent.agent_config import AgentConfig, ModelType
from prompt.callbacks.plan import create_plan_callback, validate_plan_callback
from prompt.callbacks.query_user import query_user_callback
from prompt.prompt_strategy import IPromptStrategy
from task.task import Task
from task.task_hierarchy_renderer import TaskHierarchyRenderer


class CreatePlanStrategy(IPromptStrategy):
    _TEMPLATE_NAME = "create_plan.yaml"
    _HANDLER_FUNCTIONS: Dict[str, Callable] = {
        "update_plan": create_plan_callback,
        "validate_plan": validate_plan_callback,
        "ask_user": query_user_callback,
    }

    def __init__(self, agent_role: str, reason: str = "") -> None:
        super().__init__()
        self.agent_role = agent_role
        self.reason = reason

    def get_template_name(self) -> str:
        return self._TEMPLATE_NAME

    def get_render_args(self, task: Task) -> Dict[str, Any]:
        return {
            "role": self.agent_role,
            "goal": task.goal,
            "definition": task.definition,
            "specifics": task.specifics,
            "reason": self.reason,
            "plan": task.plan,
            "task_hierarchy": TaskHierarchyRenderer.render_hierarchy(task),
            "task_root_goal": task.root().goal,
            "task_is_root": task.root().id == task.id,
        }

    def callbacks(self) -> Dict[str, Callable]:
        return self._HANDLER_FUNCTIONS

    def agent_config(self) -> AgentConfig:
        return AgentConfig(ModelType.CAPABLE, 2048, 0)
