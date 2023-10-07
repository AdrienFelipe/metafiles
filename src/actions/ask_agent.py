from action import Action
from action_result import ActionResult
from registry import action_registry
from task import Task


class AskAgent(Action):
    description = "Ask a specialized agent to address a question or task"

    def execute(self, task: Task, reason: str) -> ActionResult:
        """Apply the action given a task and a reason."""


action_registry.register_action("ask_agent", AskAgent)
