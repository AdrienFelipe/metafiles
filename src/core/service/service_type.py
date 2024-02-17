from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from core.service.service_container import ServiceContainer


class IService(ABC):
    def __init__(self, container: ServiceContainer) -> None:
        super().__init__()


TService = TypeVar("TService", bound=IService)
