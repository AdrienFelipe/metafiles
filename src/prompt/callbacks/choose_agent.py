from typing import List

from prompt.prompt_result import PromptResponse, PromptStatus
from task import Task


class ChooseAgentResponse(PromptResponse):
    def __init__(self, roles: List[str]):
        super().__init__(PromptStatus.SUCCESS, "", {"roles": roles})

    def get_roles(self) -> List[str]:
        return self.data["roles"]


def choose_agent_roles_callback(task: Task, roles: str) -> ChooseAgentResponse:
    roles_list = [role.strip() for role in roles.split(",") if role.strip() != ""]
    return ChooseAgentResponse(roles_list)
