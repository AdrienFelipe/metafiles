from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus

from action.action import Action, ActionName
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from task import Task


class RunCode(Action):
    description = "Execute a single atomic code function"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        agent_proxy = AgentProxy(agent)

        if not task.plan:
            code = agent_proxy.ask_for_code(task, reason)

        # TODO: validate code is not harmful
        # TODO: test the code on test data

        # Eval run code

        return ActionResult(ActionResultStatus.PENDING)


action_registry.register_action(ActionName.RUN_CODE, RunCode)
