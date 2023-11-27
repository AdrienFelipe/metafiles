import io
import re
import sys
import traceback
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
    description = "Perform a specific code operation"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        command = CreateCodeCommand(agent, task)
        iteration_count = 0
        execution_result = None

        while iteration_count < MAX_ITERATIONS:
            response = command.ask(reason)

            if response.status == PromptStatus.POSTPONED:
                return ActionResult(ActionResultStatus.PENDING, response.change_log())

            if response.status == PromptStatus.COMPLETED and execution_result is not None:
                return ActionResult(ActionResultStatus.SUCCESS, execution_result)

            if response.code():
                task.code = response.code()
                # TODO: test the code on test data
                # TODO: validate code is not harmful
                execution_result = self.run_code(task.code, task.context)
                command.strategy.log_execution(response.change_log(), execution_result)

            iteration_count += 1

        return ActionResult(ActionResultStatus.FAILURE, response.get_message())

    def run_code(self, code: str, context: Dict[str, Any]) -> str:
        buffer = io.StringIO()
        sys.stdout = buffer

        try:
            exec(code, context)
            printed_output = buffer.getvalue().strip()
            return printed_output
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            filtered_trace = []

            # Regex pattern for lines referencing Python files
            py_file_pattern = re.compile(r' +File +".*\.py", +line \d+.*')

            for line in stack_trace:
                # Check if the line matches the Python file reference pattern
                if py_file_pattern.match(line):
                    continue

                # Remove 'File "<string>", ' from the line if present
                if "<string>" in line:
                    line = line.replace('File "<string>", ', "")

                filtered_trace.append(line)

            formatted_stack_trace = "".join(filtered_trace).strip()
            return f"An error occurred. {formatted_stack_trace}"
        finally:
            sys.stdout = sys.__stdout__


action_registry.register_action(ActionName.RUN_CODE, RunCode)
