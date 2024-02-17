from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from action.action_name import ActionName
from core.service.service_type import IService

if TYPE_CHECKING:
    from action.action import Action


class IActionRegistry(IService):
    @abstractmethod
    def get_action(self, name: ActionName) -> Action:
        pass

    @abstractmethod
    def get_registered_actions(self):
        pass

    @abstractmethod
    def register_actions(self):
        pass
