from action.action import Action
from action.action_name import ActionName
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from task.task import Task
from task.value_objects.user_query import UserQuery


class AskUser(Action):
    action_name = ActionName.ASK_USER
    description = "Request additional information from the user. Use this sparingly, only when additional information is crucial to proceed."

    def execute(self, agent: AgentInterface, task: Task, question: str = "") -> ActionResult:
        answer = AskUser.query(task, question)
        result = f"{question}\n  {answer}"

        return ActionResult(ActionResultStatus.COMPLETED, result)

    @staticmethod
    def query(task, question: str) -> str:
        answer = input(question)
        UserQuery.add(task, question, answer)

        return answer
