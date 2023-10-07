from prompts.prompt import Prompt
from prompts.prompt_strategy import IPromptStrategy
from prompts.strategies.choose_action import ChooseActionStrategy
from prompts.strategies.choose_agent import ChooseAgentStrategy
from prompts.strategies.create_plan import CreatePlanStrategy
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
