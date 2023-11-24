from typing import Dict, Type

from core.logger.file_logger import FileLogger
from core.logger.logger_interface import IExecutionLogger
from core.service.service_type import IService

services_registry: Dict[Type[IService], Type[IService]] = {
    IExecutionLogger: FileLogger,
}
