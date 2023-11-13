import io
import sys
from typing import Any, Dict

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
        if not task.code:
            codeResponse = CreateCodeCommand.ask(agent, task, reason)
            if not codeResponse.is_successful():
                return ActionResult(ActionResultStatus.PENDING, codeResponse.get_message())
            task.code = codeResponse.get_code()

            # TODO: validate code is not harmful
            # TODO: test the code on test data

        # Eval run code
        execution_result = self.run_code(task.code)

        # TODO: validate output is what was expected

        return ActionResult(ActionResultStatus.SUCCESS, execution_result)

    def run_code(self, code: str):
        buffer = io.StringIO()
        sys.stdout = buffer

        context: Dict[str, Any] = {}
        try:
            exec(code, context)
            printed_output = buffer.getvalue().strip()
            return printed_output  # , context
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            sys.stdout = sys.__stdout__


action_registry.register_action(ActionName.RUN_CODE, RunCode)
