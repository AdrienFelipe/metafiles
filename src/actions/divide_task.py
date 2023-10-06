from registry import action_registry
from action import Action
from action_result import ActionResult
from task import Task


class DivideTask(Action):
    description = "Subdivide the task into smaller tasks"

    def apply(self, task: Task, reason: str) -> ActionResult:
        # Prompt which agents would best know about the task to know what to do
        # For each agent role
        # Prompt acting like agent to list first level of sub tasks to divide or refine it
        # Validate the answer is what was expected
        # Update task with plan
        pass


action_registry.register_action("divide_task", DivideTask)
