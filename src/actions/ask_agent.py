from registry import action_registry
from action import Action
from action_result import ActionResult
from task import Task

class AskAgent(Action):
    description = "Ask a specialized agent to address a question or task"
    
    def apply(self, task: Task, reason: str) -> ActionResult:
        """Apply the action given a task and a reason."""
        pass

action_registry.register_action('ask_agent', AskAgent)
