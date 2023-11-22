class ServiceContainer:
    def __init__(self, services):
        self.services = services
        self.instances = {}

    def get_service(self, service_key):
        if service_key not in self.services:
            raise ValueError(f"Service not found: {service_key}")
        if service_key not in self.instances:
            self.instances[service_key] = self.build_service(service_key)
        return self.instances[service_key]

    def build_service(self, service_key):
        return self.services[service_key](self.services)
