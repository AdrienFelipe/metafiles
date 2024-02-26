import pytest

from core.logger.logger_interface import IExecutionLogger
from core.logger.test_logger import TestLogger
from core.service.service_container import ServiceContainer
from core.service.service_registry import services_registry


# ServiceContainer for integration tests
@pytest.fixture(scope="function")
def container(request: pytest.FixtureRequest):
    services = services_registry.copy()
    services[IExecutionLogger] = TestLogger, request.node.name

    yield ServiceContainer(services)
    # Teardown logic here
