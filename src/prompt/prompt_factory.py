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
    def choose_action(task: Task, reason: str = "") -> Prompt[ChooseActionStrategy]:
        return PromptFactory._create(task, ChooseActionStrategy(reason))

    @staticmethod
    def choose_agent(task: Task, reason: str = "") -> Prompt[ChooseAgentStrategy]:
        return PromptFactory._create(task, ChooseAgentStrategy(reason))

    @staticmethod
    def create_plan(task: Task, role: str, reason: str = "") -> Prompt[CreatePlanStrategy]:
        return PromptFactory._create(task, CreatePlanStrategy(role, reason))

    @staticmethod
    def filter_requirements(task: Task, sub_goal: str) -> Prompt[FilterRequirementsStrategy]:
        return PromptFactory._create(task, FilterRequirementsStrategy(sub_goal))

    @staticmethod
    def create_code(task: Task) -> Prompt[CreateCodeStrategy]:
        return PromptFactory._create(task, CreateCodeStrategy())
