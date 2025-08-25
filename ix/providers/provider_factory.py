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
        return OpenAILLM(api_key=Config.OPENAI_API_KEY, model_name=Config.OPENAI_MODEL_NAME)
    else:
        raise InvalidProviderError(f"Invalid provider: {Config.PROVIDER}")
