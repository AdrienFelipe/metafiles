import io
import sys

from action.action import Action
from action.action_name import ActionName
from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from prompt.commands.create_code_command import CreateCodeCommand
from task.task import Task


class RunCode(Action):
    description = "Execute a single atomic code function"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        if not task.plan:
            task.plan = [CreateCodeCommand.ask(agent, task, reason).get_code()]

        # TODO: validate code is not harmful
        # TODO: test the code on test data

        # Eval run code
        result = self.run_code("\n\n".join(task.plan))

        # TODO: validate output is what was expected

        return ActionResult(ActionResultStatus.SUCCESS, result)

    def run_code(self, code: str):
        buffer = io.StringIO()
        sys.stdout = buffer

        context = {}
        try:
            exec(code, context)
            printed_output = buffer.getvalue().strip()
            return printed_output  # , context
        finally:
            sys.stdout = sys.__stdout__


action_registry.register_action(ActionName.RUN_CODE, RunCode)
