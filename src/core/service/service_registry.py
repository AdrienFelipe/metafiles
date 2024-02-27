from typing import Dict, Tuple, Type

from action.action_registry import ActionRegistry
from action.action_registry_interface import IActionRegistry
from core.logger.file_logger import FileLogger
from core.logger.logger_interface import IExecutionLogger
from core.service.service_type import IService
from prompt.context.in_memory_context import InMemoryContext
from prompt.context.prompt_context_interface import IPromptContext
from task.task_handler import TaskHandler
from task.task_handler_interface import ITaskHandler

services_registry: Dict[Type[IService], Tuple[Type[IService], ...]] = {
    IExecutionLogger: (FileLogger,),
    ITaskHandler: (TaskHandler,),
    IPromptContext: (InMemoryContext,),
    IActionRegistry: (ActionRegistry,),
}
