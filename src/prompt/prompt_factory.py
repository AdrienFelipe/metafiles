from prompt.prompt import Prompt
from prompt.prompt_strategy import IPromptStrategy
from prompt.strategies.choose_action import ChooseActionStrategy
from prompt.strategies.choose_agent import ChooseAgentStrategy
from prompt.strategies.create_code import CreateCodeStrategy
from prompt.strategies.create_plan import CreatePlanStrategy
from prompt.strategies.filter_requirements import FilterRequirementsStrategy
from task import Task


class PromptFactory:
    @staticmethod
    def _create(task: Task, strategy: IPromptStrategy) -> Prompt:
        return Prompt(task, strategy)

    @staticmethod
    def choose_action(task: Task) -> Prompt:
        return PromptFactory._create(task, ChooseActionStrategy())

    @staticmethod
    def choose_agent(task: Task) -> Prompt:
        return PromptFactory._create(task, ChooseAgentStrategy())

    @staticmethod
    def create_plan(task: Task, role: str) -> Prompt:
        return PromptFactory._create(task, CreatePlanStrategy(role))

    @staticmethod
    def filter_requirements(task: Task, sub_goal: str) -> Prompt:
        return PromptFactory._create(task, FilterRequirementsStrategy(sub_goal))

    @staticmethod
    def create_code(task: Task, reason: str) -> Prompt:
        return PromptFactory._create(task, CreateCodeStrategy(reason))
