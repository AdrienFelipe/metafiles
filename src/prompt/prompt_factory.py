from prompt.prompt import Prompt
from prompt.prompt_strategy import TStrategy
from prompt.strategies.choose_action import ChooseActionStrategy
from prompt.strategies.choose_agent import ChooseAgentStrategy
from prompt.strategies.create_code import CreateCodeStrategy
from prompt.strategies.create_plan import CreatePlanStrategy
from prompt.strategies.filter_requirements import FilterRequirementsStrategy
from task.task import Task


class PromptFactory:
    @staticmethod
    def _create(task: Task, strategy: TStrategy) -> Prompt[TStrategy]:
        return Prompt(task, strategy)

    @staticmethod
    def choose_action(task: Task) -> Prompt[ChooseActionStrategy]:
        return PromptFactory._create(task, ChooseActionStrategy())

    @staticmethod
    def choose_agent(task: Task) -> Prompt[ChooseAgentStrategy]:
        return PromptFactory._create(task, ChooseAgentStrategy())

    @staticmethod
    def create_plan(task: Task, role: str) -> Prompt[CreatePlanStrategy]:
        return PromptFactory._create(task, CreatePlanStrategy(role))

    @staticmethod
    def filter_requirements(task: Task, sub_goal: str) -> Prompt[FilterRequirementsStrategy]:
        return PromptFactory._create(task, FilterRequirementsStrategy(sub_goal))

    @staticmethod
    def create_code(task: Task, reason: str) -> Prompt[CreateCodeStrategy]:
        return PromptFactory._create(task, CreateCodeStrategy(reason))
