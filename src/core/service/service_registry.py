from core.logger.file_logger import FileLogger
from core.logger.logger_interface import IExecutionLogger


services_registry = {
    IExecutionLogger: FileLogger,
}