from action.action_registry import action_registry
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from core.logger.logger_interface import IExecutionLogger
from prompt.commands.review_result_command import ReviewResultCommand
from task.task import Task

MAX_ITERATIONS = 10
# Name the modulo 3 to remove the action
ACTION_RESET_MODULO = 3


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

        while iteration_count < MAX_ITERATIONS:
            if task.action:
                action_name = task.action
            else:
                response = agent_proxy.ask_to_choose_action(task, reason)
                action_name, reason = response.action_name(), response.reason()

            self._logger.log(f"🕹️ Action: {action_name}")

            # TODO: validate action is valid (not NO_ACTION)

            # Now with task type, execute it's action
            task.result = action_registry.get_action(action_name).execute(agent, task, reason)
            result_review = ReviewResultCommand(agent, task).ask()

            if result_review.is_completed():
                break

            reason = result_review.reason()
            if iteration_count % ACTION_RESET_MODULO == 0:
                task.action = None
            iteration_count += 1

        self._logger.log(
            f"{task.result.status.icon} Execution result: [{task.id}]\n{task.result.message}"
        )
