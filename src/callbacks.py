from typing import List

from task import Task


def choose_action_callback(task: Task, action_key: str, reason: str) -> (str, str):
    """
    Returns:
    - action_key: The key or identifier for the chosen action
    - reason: The reason or justification for the chosen action
    """
    return action_key, reason


def choose_agent_roles_callback(task: Task, roles: str) -> List[str]:
    return [role.strip() for role in roles.split(",") if role.strip() != ""]


def create_plan_parse_callback(task: Task, plan: str) -> List[str]:
    return plan.splitlines()


def query_user_callback(task: Task, query: str) -> str:
    return query
