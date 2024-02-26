from action.action import Action
from action.action_name import ActionName
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from task.task import Task


class NoAction(Action):
    action_name = ActionName.NO_ACTION
    description = "Do nothing. Select this if no further action is required on the current task."

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> ActionResult:
        return ActionResult(ActionResultStatus.COMPLETED)
