from action.action import Action
from action.action_name import ActionName
from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from task import Task


class NoAction(Action):
    description = "Do nothing"

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        return ActionResult(ActionResultStatus.SUCCESS)


action_registry.register_action(ActionName.NO_ACTION, NoAction)
