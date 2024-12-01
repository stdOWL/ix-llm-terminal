from .llama_llm import LocalLLM
from .openai_llm import OpenAILLM
from ix.exceptions import InvalidProviderError
from ix.config import Config


def get_provider():
    """
    Factory method to get the appropriate LLM provider.
    """
    if Config.PROVIDER == "local":
        return LocalLLM()
    elif Config.PROVIDER == "openai":
        return OpenAILLM()
    else:
        raise InvalidProviderError(f"Invalid provider: {Config.PROVIDER}")
