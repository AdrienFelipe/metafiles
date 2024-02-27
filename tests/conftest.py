import pytest

from core.logger.logger_interface import IExecutionLogger
from core.service.service_container import ServiceContainer
from main import bootstrap
from prompt.context.prompt_context_interface import IPromptContext
from task.task_handler_interface import ITaskHandler


@pytest.fixture(scope="session", autouse=True)
def app_bootstrap():
    bootstrap()


@pytest.fixture(scope="function")
def logger(container: ServiceContainer):
    return container.get_service(IExecutionLogger)


@pytest.fixture(scope="function")
def task_handler(container: ServiceContainer):
    return container.get_service(ITaskHandler)


@pytest.fixture(scope="function")
def prompt_context(container: ServiceContainer):
    return container.get_service(IPromptContext)
