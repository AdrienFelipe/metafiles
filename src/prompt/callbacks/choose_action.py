from typing import Union

from action.action_name import ActionName
from prompt.prompt_result import InvalidPromptResponse, PromptResponse, PromptStatus
from task import Task


class ChooseActionResponse(PromptResponse):
    def __init__(self, action: ActionName, reason: str):
        data = {"action": action, "reason": reason}
        super().__init__(PromptStatus.SUCCESS, action.value, data)

    def get_action(self) -> ActionName:
        return self.data["action"]

    def get_reason(self) -> str:
        return self.data["reason"]


def choose_action_callback(
    task: Task, action_key: str, reason: str
) -> Union[ChooseActionResponse, InvalidPromptResponse]:
    if action_key not in ActionName._value2member_map_:
        return InvalidPromptResponse(f"Invalid action name: {action_key}")

    return ChooseActionResponse(ActionName(action_key), reason)
