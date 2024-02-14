from action.action_registry import action_registry
from action.action_result import ActionResult, ActionResultStatus
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from core.logger.logger_interface import IExecutionLogger
from prompt.commands.review_result_command import ReviewResultCommand
from task.task import Task

MAX_ITERATIONS = 10


class TaskHandler:
    def __init__(self, logger: IExecutionLogger):
        self._logger = logger

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> None:
        self._logger.log(
            f"⚙️ Executing task [{task.id}]",
            {"goal": task.goal, "definition": task.definition, "specifics": task.specifics},
        )
        agent_proxy = AgentProxy(agent)
        iteration_count = 0

        while not task.result.is_completed() and iteration_count < MAX_ITERATIONS:
            if not task.action:
                response = agent_proxy.ask_to_choose_action(task, reason)
                task.action, reason = response.action_name(), response.reason()

            self._logger.log(f"🕹️ Action: {task.action}")

            try:
                # Now with task type, execute it's action
                task.result = action_registry.get_action(task.action).execute(agent, task, reason)
            except Exception as e:
                self._logger.log(f"💥 Exception: {e}")
                task.result = ActionResult(ActionResultStatus.FAILURE, str(e))

            if task.result.is_completed():
                result_review = ReviewResultCommand(agent, task).ask()

                if result_review.is_ok():
                    continue

                task.result.status = ActionResultStatus.PENDING
                reason = result_review.reason()
            else:
                reason = task.result.message

            iteration_count += 1

        self._logger.log(
            f"{task.result.status.icon} Execution result: [{task.id}]\n{task.result.message}"
        )
