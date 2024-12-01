import openai
from .base import LLM


class OpenAILLM(LLM):
    """
    Implementation of the LLM interface for OpenAI models.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("OpenAI LLM generation is not yet implemented.")

    def is_ready(self) -> bool:
        return bool(self.api_key)
