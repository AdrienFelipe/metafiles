from dotenv import load_dotenv

from action.action_registry import action_registry
from agent.agents.openai_agent import OpenAIAgent
from core.logger.logger_interface import IExecutionLogger
from core.service.service_container import ServiceContainer
from core.service.service_registry import services_registry
from task.task import Task
from task.task_handler import TaskHandler


def bootstrap() -> None:
    load_dotenv()
    action_registry.register_actions()


def main() -> None:
    bootstrap()
    container = ServiceContainer(services_registry)
    logger = container.get_service(IExecutionLogger)

    agent = OpenAIAgent(logger)
    task = Task.from_yaml("/data/file_index.yaml")
    TaskHandler(logger).execute(agent, task)


if __name__ == "__main__":
    main()
