from typing import List, NamedTuple

from prompt.prompt_result import PromptResponse, PromptStatus
from task import Task


class InvalidPromptResponse(PromptResponse):
    def __init__(self, message: str):
        super().__init__(PromptStatus.FAILURE, message)


class ChooseAgentResponse(NamedTuple):
    roles: List[str]


def choose_agent_roles_callback(task: Task, roles: str) -> ChooseAgentResponse:
    roles_list = [role.strip() for role in roles.split(",") if role.strip() != ""]
    return ChooseAgentResponse(roles_list)


class CreatePlanResponse(NamedTuple):
    plan_lines: List[str]


def create_plan_parse_callback(task: Task, plan: str) -> CreatePlanResponse:
    lines = [line.strip() for line in plan.splitlines() if line.strip()]
    return CreatePlanResponse(lines)


class ValidatePlanResponse(NamedTuple):
    plan_lines: List[str]


def validate_plan_callback(task: Task, plan: str) -> ValidatePlanResponse:
    lines = [line.strip() for line in plan.splitlines() if line.strip()]
    return ValidatePlanResponse(lines)


class QueryUserResponse(NamedTuple):
    query: str


def query_user_callback(task: Task, query: str) -> QueryUserResponse:
    return QueryUserResponse(query)


class CreateCodeResponse(NamedTuple):
    message: str


def create_code_callback(task: Task, code: str) -> CreateCodeResponse:
    return CreateCodeResponse(code)
