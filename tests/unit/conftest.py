import pytest

from core.logger.logger_interface import IExecutionLogger
from core.logger.no_logger import NoLogger
from core.service.service_container import ServiceContainer
from core.service.service_registry import services_registry


@pytest.fixture(scope="function")
def container():
    services = services_registry
    services[IExecutionLogger] = NoLogger
    container = ServiceContainer(services)
    # Configure container for unit tests with mocks/stubs
    # e.g., container.add_service('Database', MockDatabaseService())
    yield container
    # Teardown logic here
