import json
from typing import List

import yaml

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class CreatePlanResponse(PromptResponse):
    def __init__(
        self, plan: List[str], status: PromptStatus = PromptStatus.SUCCESS, message: str = ""
    ):
        super().__init__(status, message, {"plan": plan})

    def get_plan(self) -> List[str]:
        return self.data["plan"]


def create_plan_callback(task: Task, plan: str) -> CreatePlanResponse:
    text_plan = [yaml.dump(step, sort_keys=False, width=999).strip() for step in json.loads(plan)]
    return CreatePlanResponse(text_plan)


class ValidatePlanResponse(CreatePlanResponse):
    pass


def validate_plan_callback(task: Task) -> ValidatePlanResponse:
    return ValidatePlanResponse(task.plan)


class FailedCreatePlanResponse(CreatePlanResponse):
    def __init__(self, message: str):
        super().__init__([], PromptStatus.FAILURE, message)
