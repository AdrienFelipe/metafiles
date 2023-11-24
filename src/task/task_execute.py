from action.action_registry import action_registry
from agent.agent_interface import AgentInterface
from agent.agent_proxy import AgentProxy
from core.logger.logger_interface import IExecutionLogger
from core.service.service_container import ServiceContainer
from core.service.service_registry import services_registry
from task.task import Task

MAX_ITERATIONS = 10


class TaskHandler:
    def __init__(self, logger: IExecutionLogger):
        self._logger = logger

    def execute(self, agent: AgentInterface, task: Task, reason: str = "") -> None:
        self._logger.log(f"Executing task: [{task.id}] {task.goal}")
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


def execute_task(agent: AgentInterface, task: Task, reason: str = "") -> None:
    logger = ServiceContainer(services_registry).get_service(IExecutionLogger)
    TaskHandler(logger).execute(agent, task, reason)
