from typing import List

from core.service.service_container import ServiceContainer
from prompt.context.abstract_prompt_context import AbstractPromptContext
from prompt.context.interaction import Interaction


class InMemoryContext(AbstractPromptContext):
    def __init__(self, container: ServiceContainer) -> None:
        super().__init__(container)
        self.interactions: List[Interaction] = []

    def _add_interaction(self, interaction: Interaction) -> None:
        self.interactions.append(interaction)

    def get_interactions(self) -> List[Interaction]:
        return self.interactions
