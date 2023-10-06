from registry import action_registry
from action import Action
from action_result import ActionResult
from task import Task


class AskUser(Action):
    description = "Ask the user for clarification about their goal"

    def apply(self, task: Task, reason: str) -> ActionResult:
        """Apply the action given a task and a reason."""
        pass


action_registry.register_action("ask_user", AskUser)
