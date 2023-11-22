from core.logger.file_logger import FileLogger
from task.task_execute import TaskManager

services_registry = {"ExecutionLogger": FileLogger, "TaskManager": TaskManager}
