from abc import abstractmethod


class AgentInterface:
    @abstractmethod
    def ask(self, prompt: str) -> str:
        """Ask a question to the agent and return the response."""
