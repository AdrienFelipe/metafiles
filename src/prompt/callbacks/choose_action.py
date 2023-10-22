from typing import Union

from action.action_name import ActionName
from prompt.prompt_result import FailedPromptResponse, PromptResponse, PromptStatus
from task.task import Task


class ChooseActionResponse(PromptResponse):
    def __init__(
        self, action: ActionName, reason: str, status: PromptStatus = PromptStatus.SUCCESS
    ):
        data = {"action": action, "reason": reason}
        super().__init__(status, action.value, data)

    def get_action_name(self) -> ActionName:
        return self.data["action"]

    def get_reason(self) -> str:
        return self.data["reason"]


class FailedChooseActionResponse(ChooseActionResponse):
    def __init__(self, reason: str):
        super().__init__(ActionName.NO_ACTION, reason, PromptStatus.FAILURE)


def choose_action_callback(
    task: Task, action_key: str, reason: str
) -> Union[ChooseActionResponse, FailedPromptResponse]:
    if action_key not in ActionName._value2member_map_:
        return FailedPromptResponse(f"Invalid action name: {action_key}")

    return ChooseActionResponse(ActionName(action_key), reason)
