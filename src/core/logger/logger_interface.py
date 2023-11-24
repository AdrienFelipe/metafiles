from abc import abstractmethod

from core.service.service_container import IService


class IExecutionLogger(IService):
    @abstractmethod
    def log(self, message: str):
        pass
