from abc import ABC
from typing import TypeVar


class IService(ABC):
    pass


TService = TypeVar("TService", bound=IService)
