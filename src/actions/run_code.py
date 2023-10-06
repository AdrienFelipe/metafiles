from registry import action_registry
from action import Action
from action_result import ActionResult
from task import Task

class RunCode(Action):
    description = "Execute a single atomic code function"
    
    def apply(self, task: Task, reason: str) -> ActionResult:
        """Apply the action given a task and a reason."""
        pass

action_registry.register_action('run_code', RunCode)
