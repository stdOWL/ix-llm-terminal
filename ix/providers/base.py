from abc import ABC, abstractmethod


class LLM(ABC):
    """
    Abstract base class for LLM implementations.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response based on the given prompt.
        """
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """
        Check if the LLM is ready for use.
        """
        pass
