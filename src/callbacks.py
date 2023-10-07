from typing import List, NamedTuple

from task import Task


class ChooseActionResponse(NamedTuple):
    action_key: str
    reason: str


def choose_action_callback(task: Task, action_key: str, reason: str) -> ChooseActionResponse:
    return ChooseActionResponse(action_key, reason)


class ChooseAgentResponse(NamedTuple):
    roles: List[str]


def choose_agent_roles_callback(task: Task, roles: str) -> ChooseAgentResponse:
    roles_list = [role.strip() for role in roles.split(",") if role.strip() != ""]
    return ChooseAgentResponse(roles_list)


class CreatePlanResponse(NamedTuple):
    plan_lines: List[str]


def create_plan_parse_callback(task: Task, plan: str) -> CreatePlanResponse:
    return CreatePlanResponse(plan.splitlines())


class QueryUserResponse(NamedTuple):
    query: str


def query_user_callback(task: Task, query: str) -> QueryUserResponse:
    return QueryUserResponse(query)


class ValidatePlanResponse(NamedTuple):
    pass


def validate_plan_callback(task: Task) -> ValidatePlanResponse:
    return ValidatePlanResponse()
