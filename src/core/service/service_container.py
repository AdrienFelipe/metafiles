from typing import Dict, Type

from core.service.service_type import IService, TService


class ServiceContainer:
    def __init__(self, services_registry: Dict[Type[IService], Type[TService]]):
        self._services_registry = services_registry
        self._instances: Dict[Type[TService], TService] = {}

    def get_service(self, service_key: Type[TService]) -> TService:
        if service_key not in self._instances:
            self._instances[service_key] = self._services_registry[service_key]()

        return self._instances[service_key]
