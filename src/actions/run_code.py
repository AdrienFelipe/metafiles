from action import Action
from action_result import ActionResult
from agent_proxy import AgentProxy
from registry import action_registry
from task import Task


class RunCode(Action):
    description = "Execute a single atomic code function"

    def execute(self, task: Task, reason: str = "") -> ActionResult:
        if not task.plan:
            code = AgentProxy.ask_for_code(task, reason)

        # TODO: validate code is not harmful
        # TODO: test the code on test data

        # Eval run code


action_registry.register_action("run_code", RunCode)
