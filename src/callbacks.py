from typing import List
from registry import action_registry
from action_result import ActionResult
from task import Task


def execute_action(task: Task, action_key: str, reason: str) -> ActionResult:
    return action_registry.get_action(action_key).execute(task, reason)


def ask_agents(task: Task, roles: str) -> List[str]:
    return [role.strip() for role in roles.split(",") if role.strip() != ""]


def update_plan(task: Task, plan: str) -> List[str]:
    print(plan)
    return plan
