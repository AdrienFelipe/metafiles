from abc import abstractmethod
from typing import Dict, Optional

from core.service.service_container import IService


class IExecutionLogger(IService):
    @abstractmethod
    def log(self, message: str, data: Optional[Dict] = None, exc: Optional[Exception] = None):
        pass
