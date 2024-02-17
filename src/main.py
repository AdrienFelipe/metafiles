from dotenv import load_dotenv

from action.action_registry import ActionRegistry
from agent.agents.openai_agent import OpenAIAgent
from core.logger.logger_interface import IExecutionLogger
from core.service.service_container import ServiceContainer
from core.service.service_registry import services_registry
from task.task import Task
from task.task_handler_interface import ITaskHandler


def bootstrap() -> None:
    load_dotenv()
    ActionRegistry.register_actions()


def main() -> None:
    bootstrap()
    container = ServiceContainer(services_registry)
    logger = container.get_service(IExecutionLogger)
    taskHandler = container.get_service(ITaskHandler)

    agent = OpenAIAgent(logger)
    task = Task.from_yaml("/data/file_index.yaml")
    taskHandler.execute(agent, task)


if __name__ == "__main__":
    main()
