from typing import Dict, Type

from core.service.service_type import IService, TService


class ServiceContainer:
    def __init__(self, services_registry: Dict[Type[IService], Type[TService]]):
        self.services_registry = services_registry

    def get_service(self, service_key: Type[TService]) -> TService:
        service_class = self.services_registry[service_key]
        return service_class()
