from typing import TypeVar, Generic, Dict, Type

T = TypeVar('T')  # Generic type variable

class ServiceContainer:
    def __init__(self, services: Dict[Type[T], T]):
        self.services: Dict[Type[T], T] = services
        self.instances: Dict[Type[T], T] = {}

    def get_service(self, service_type: Type[T]) -> T:
        if service_type not in self.services:
            raise ValueError(f"Service not found for type: {service_type.__name__}")
        
        if service_type not in self.instances:
            self.instances[service_type] = self.build_service(service_type)
            
        return self.instances[service_type]

    def build_service(self, service_type: Type[T]) -> T:
        return self.services[service_type]()
