from prompt.context.prompt_context_interface import IPromptContext
from prompt.prompt import Prompt
from prompt.prompt_strategy import TStrategy
from prompt.strategies.choose_action import ChooseActionStrategy
from prompt.strategies.choose_agent import ChooseAgentStrategy
from prompt.strategies.create_code import CreateCodeStrategy
from prompt.strategies.create_plan import CreatePlanStrategy
from task.task import Task


class PromptFactory:
    @staticmethod
    def _create(task: Task, strategy: TStrategy, context: IPromptContext) -> Prompt[TStrategy]:
        return Prompt(task, strategy, context)

    @staticmethod
    def choose_action(
        task: Task, context: IPromptContext, reason: str = ""
    ) -> Prompt[ChooseActionStrategy]:
        return PromptFactory._create(task, ChooseActionStrategy(reason), context)

    @staticmethod
    def choose_agent(
        task: Task, context: IPromptContext, reason: str = ""
    ) -> Prompt[ChooseAgentStrategy]:
        return PromptFactory._create(task, ChooseAgentStrategy(reason), context)

    @staticmethod
    def create_plan(
        task: Task, context: IPromptContext, role: str, reason: str = ""
    ) -> Prompt[CreatePlanStrategy]:
        return PromptFactory._create(task, CreatePlanStrategy(role, reason), context)

    @staticmethod
    def create_code(task: Task, context: IPromptContext) -> Prompt[CreateCodeStrategy]:
        return PromptFactory._create(task, CreateCodeStrategy(), context)
