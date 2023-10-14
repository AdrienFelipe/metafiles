from enum import Enum, auto


class ModelType(Enum):
    FAST = auto()
    CAPABLE = auto()


class AgentConfig:
    def __init__(self, model: ModelType, max_tokens: int, temperature: int):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
