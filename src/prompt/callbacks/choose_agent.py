from prompt.prompt_result import PromptResponse, PromptStatus
from task.task import Task


class ChooseAgentResponse(PromptResponse):
    def __init__(self, roles: str, status: PromptStatus = PromptStatus.OK, message: str = ""):
        super().__init__(status, message, {"roles": roles})

    def get_roles(self) -> str:
        return self.data["roles"]


class FailedChooseAgentResponse(ChooseAgentResponse):
    def __init__(self, message: str):
        super().__init__("", PromptStatus.FAILURE, message)


def choose_agent_roles_callback(task: Task, roles: str) -> ChooseAgentResponse:
    return ChooseAgentResponse(roles.strip())
