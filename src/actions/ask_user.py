from action import Action
from action_registry import action_registry
from action_result import ActionResult
from task import Task


class AskUser(Action):
    description = "Ask the user for clarification about their goal"

    def execute(self, task: Task, reason: str = "") -> ActionResult:
        """Apply the action given a task and a reason."""


action_registry.register_action("ask_user", AskUser)
