from typing import List

from prompt.prompt_result import PromptResponse, PromptStatus
from task import Task


class CreatePlanResponse(PromptResponse):
    def __init__(
        self, plan: List[str], status: PromptStatus = PromptStatus.SUCCESS, message: str = ""
    ):
        super().__init__(status, message, {"plan": plan})

    def get_plan(self) -> List[str]:
        return self.data["plan"]


def create_plan_callback(task: Task, plan: str) -> CreatePlanResponse:
    lines = [line.strip() for line in plan.splitlines() if line.strip()]
    return CreatePlanResponse(lines)


class ValidatePlanResponse(CreatePlanResponse):
    pass


def validate_plan_callback(task: Task, plan: str) -> ValidatePlanResponse:
    lines = [line.strip() for line in plan.splitlines() if line.strip()]
    return ValidatePlanResponse(lines)


class FailedCreatePlanResponse(CreatePlanResponse):
    def __init__(self, message: str):
        super().__init__([], PromptStatus.FAILURE, message)
