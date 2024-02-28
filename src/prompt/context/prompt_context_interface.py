from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from core.service.service_type import IService

if TYPE_CHECKING:
    from prompt.prompt import Prompt
    from prompt.prompt_result import PromptResponse


class IPromptContext(IService, ABC):
    @abstractmethod
    def add_agent_query(self, prompt: Prompt, response: PromptResponse) -> None:
        pass

    @abstractmethod
    def get_interactions(self) -> list:
        pass
