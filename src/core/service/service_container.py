from typing import Dict, Tuple, Type

from core.service.service_type import IService, TService


class ServiceContainer:
    def __init__(self, services_registry: Dict[Type[IService], Tuple[Type[TService], ...]]):
        self._services_registry = services_registry
        self._instances: Dict[Type[TService], TService] = {}

    def get_service(self, service_key: Type[TService]) -> TService:
        if service_key not in self._instances:
            # Unpack the service class and any arguments from the tuple
            service_class, *args = self._services_registry[service_key]
            # Instantiate the service with the provided arguments
            self._instances[service_key] = service_class(self, *args)

        return self._instances[service_key]
