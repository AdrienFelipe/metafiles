import json
from typing import List

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class CreatePlanResponse(PromptResponse):
    def __init__(self, plan: List[str], status: PromptStatus = PromptStatus.OK, message: str = ""):
        super().__init__(status, message, {"plan": plan})

    def get_plan(self) -> List[str]:
        return self.data["plan"]


def create_plan_callback(task: Task, plan: str) -> CreatePlanResponse:
    plan_data = json.loads(plan)
    text_plan = [
        Task.to_plan_step(
            goal=step["goal"],
            definition=step["definition"],
            specifics=step.get("specifics"),
            depends_on=step.get("depends_on"),
        )
        for step in plan_data
    ]

    return CreatePlanResponse(text_plan)


class ValidatePlanResponse(CreatePlanResponse):
    pass


def validate_plan_callback(task: Task) -> ValidatePlanResponse:
    return ValidatePlanResponse(task.plan)


class FailedCreatePlanResponse(CreatePlanResponse):
    def __init__(self, message: str):
        super().__init__([], PromptStatus.FAILURE, message)
