from action.action_registry import action_registry
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from core.logger.logger_interface import IExecutionLogger
from core.service.service_container import ServiceContainer
from task.task import Task

MAX_ITERATIONS = 10


class TaskManager(ServiceContainer):
    def __init__(self, services):
        super().__init__(services)
        self._logger: IExecutionLogger = self.get_service("ExecutionLogger")

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> None:
        self._logger.log(f"Executing task: [{task.id}] {task.goal}")
        execute_task(agent, task, reason)


def execute_task(agent: AgentInterface, task: Task, reason: str = "") -> None:
    agent_proxy = AgentProxy(agent)
    iteration_count = 0

    while not task.result.is_successful() and iteration_count < MAX_ITERATIONS:
        if task.action:
            action_name = task.action
        else:
            response = agent_proxy.ask_to_choose_action(task, reason)
            action_name, reason = response.action_name(), response.reason()

        # TODO: validate action is valid (not NO_ACTION)

        # Now with task type, execute it's action
        task.result = action_registry.get_action(action_name).execute(agent, task, reason)
        # TODO: check task result status (success, pending, error, ...)
        reason = task.result.message

        # TODO: is goal complete?
        iteration_count += 1
