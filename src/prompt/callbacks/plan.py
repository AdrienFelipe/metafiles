import json
from typing import List

from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class CreatePlanResponse(PromptResponse):
    def __init__(
        self, plan: List[str], status: PromptStatus = PromptStatus.SUCCESS, message: str = ""
    ):
        super().__init__(status, message, {"plan": plan})

    def get_plan(self) -> List[str]:
        return self.data["plan"]


def create_plan_callback(task: Task, plan: List[dict]) -> List[str]:
    plan_list = []
    
    for task in json.loads(plan):
        task_line = f"{task['goal']}:\n{task['specifications']}"
        
        if 'depends_on' in task and task['depends_on']:
            depends_on_str = ", ".join(map(str, task['depends_on']))
            task_line += f"\ndepends on: {depends_on_str}"
        
        plan_list.append(task_line)
    
    return plan_list


class ValidatePlanResponse(CreatePlanResponse):
    pass


def validate_plan_callback(task: Task) -> ValidatePlanResponse:
    return ValidatePlanResponse(task.plan)


class FailedCreatePlanResponse(CreatePlanResponse):
    def __init__(self, message: str):
        super().__init__([], PromptStatus.FAILURE, message)
