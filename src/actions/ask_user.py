from action import Action, ActionName
from action_registry import action_registry
from action_result import ActionResult, ActionResultStatus
from agent_interface import AgentInterface
from agent_proxy import AgentProxy
from task import Task


class AskUser(Action):
    description = "Ask the user for clarification about their goal"


def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
    agent_proxy = AgentProxy(agent)
    return ActionResult(ActionResultStatus.PENDING)


action_registry.register_action(ActionName.ASK_USER, AskUser)
