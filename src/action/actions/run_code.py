import io
import sys

from action.action import Action
from action.action_name import ActionName
from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from task.task import Task


class RunCode(Action):
    description = "Execute a single atomic code function"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        agent_proxy = AgentProxy(agent)

        if not task.plan:
            task.plan = [agent_proxy.ask_for_code(task, reason).get_code()]

        # TODO: validate code is not harmful
        # TODO: test the code on test data

        # Eval run code
        result = self.run_code("\n\n".join(task.plan))

        # TODO: validate output is what was expected

        return ActionResult(ActionResultStatus.SUCCESS, result)

    def run_code(self, code: str) -> str:
        buffer = io.StringIO()
        sys.stdout = buffer
        try:
            eval(code)
            return buffer.getvalue().strip()
        finally:
            sys.stdout = sys.__stdout__


action_registry.register_action(ActionName.RUN_CODE, RunCode)
