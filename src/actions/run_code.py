from action import Action
from action_result import ActionResult
from registry import action_registry
from task import Task


class RunCode(Action):
    description = "Execute a single atomic code function"

    def execute(self, task: Task, reason: str) -> ActionResult:
        """Apply the action given a task and a reason."""


action_registry.register_action("run_code", RunCode)
