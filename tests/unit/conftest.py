from copy import deepcopy

import pytest

from core.logger.logger_interface import IExecutionLogger
from core.logger.no_logger import NoLogger
from core.service.service_container import ServiceContainer
from core.service.service_registry import services_registry


@pytest.fixture(scope="function")
def container():
    services = deepcopy(services_registry)
    services[IExecutionLogger] = (NoLogger,)

    yield ServiceContainer(services)
    # Teardown logic here
