from typing import Dict, Type

from action.action_registry import ActionRegistry
from action.action_registry_interface import IActionRegistry
from core.context.context_interface import IContext
from core.context.in_memory_context import InMemoryContext
from core.logger.file_logger import FileLogger
from core.logger.logger_interface import IExecutionLogger
from core.service.service_type import IService
from task.task_handler import TaskHandler
from task.task_handler_interface import ITaskHandler

services_registry: Dict[Type[IService], Type[IService]] = {
    IExecutionLogger: FileLogger,
    ITaskHandler: TaskHandler,
    IContext: InMemoryContext,
    IActionRegistry: ActionRegistry,
}
