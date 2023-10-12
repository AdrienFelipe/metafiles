from prompts.prompt import Prompt
from prompts.prompt_strategy import IPromptStrategy
from prompts.strategies.choose_action import ChooseActionStrategy
from prompts.strategies.choose_agent import ChooseAgentStrategy
from prompts.strategies.create_code import CreateCodeStrategy
from prompts.strategies.create_plan import CreatePlanStrategy
from prompts.strategies.filter_requirements import FilterRequirementsStrategy
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
    def ask_for_code(task: Task, reason: str) -> Prompt:
        return PromptFactory._create(task, CreateCodeStrategy(reason))
