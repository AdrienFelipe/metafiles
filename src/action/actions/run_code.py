import io
import sys
from typing import Any, Dict

from action.action import Action
from action.action_name import ActionName
from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from prompt.commands.create_code_command import CreateCodeCommand
from prompt.prompt_result import PromptStatus
from task.task import Task

MAX_ITERATIONS = 20


class RunCode(Action):
    description = "Execute a single atomic code function"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        command = CreateCodeCommand(agent, task)
        iteration_count = 0

        while iteration_count < MAX_ITERATIONS:
            if task.code:
                # TODO: test the code on test data
                # TODO: validate code is not harmful
                execution_result = self.run_code(task.code)
                command.strategy.add_execution_result(execution_result)

            response = command.ask(reason)

            if response.status == PromptStatus.POSTPONED:
                return ActionResult(ActionResultStatus.PENDING, response.get_message())

            task.code = response.get_code()
            reason = response.reason()

            if response.status == PromptStatus.COMPLETED:
                return ActionResult(ActionResultStatus.SUCCESS, response.get_message())

        return ActionResult(ActionResultStatus.FAILURE, execution_result)

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
