import pytest

from core.logger.logger_interface import IExecutionLogger
from core.logger.test_logger import TestLogger
from core.service.service_container import ServiceContainer
from main import bootstrap
from task.task_handler_interface import ITaskHandler


@pytest.fixture(scope="session", autouse=True)
def app_bootstrap():
    bootstrap()


@pytest.fixture(scope="function")
def logger(container: ServiceContainer, request: pytest.FixtureRequest):
    _logger = container.get_service(IExecutionLogger)

    if isinstance(_logger, TestLogger):
        # Add the name of the current test function as subdir
        _logger.add_subdir(request.node.name)

    return _logger


@pytest.fixture(scope="function")
def task_handler(container: ServiceContainer):
    return container.get_service(ITaskHandler)
