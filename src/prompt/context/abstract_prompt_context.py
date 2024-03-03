from abc import ABC, abstractmethod

from core.service.service_container import ServiceContainer
from prompt.context.interaction import Interaction, InteractionType
from prompt.context.prompt_context_interface import IPromptContext
from prompt.prompt import Prompt
from prompt.prompt_result import PromptResponse


class AbstractPromptContext(IPromptContext, ABC):
    def __init__(self, container: ServiceContainer) -> None:
        super().__init__(container)

    @abstractmethod
    def _add_interaction(self, interaction: Interaction) -> None:
        pass

    def add_agent_query(self, prompt: Prompt, response: PromptResponse) -> None:
        prompt_type = prompt.strategy.__class__.__name__
        response_type = response.__class__.__name__
        message = response.message.replace("\n", " ")
        if len(message) > 100:
            message = response.message[:97] + "..."

        message = f'{prompt_type} > {response_type}: "{message}"'

        interaction = Interaction(
            InteractionType.AGENT_QUERY, prompt.task, message, response.status.name
        )
        self._add_interaction(interaction)
