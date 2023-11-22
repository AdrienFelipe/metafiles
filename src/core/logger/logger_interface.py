from abc import ABCMeta, abstractmethod


class IExecutionLogger(metaclass=ABCMeta):
    @abstractmethod
    def log(self, message: str):
        pass
