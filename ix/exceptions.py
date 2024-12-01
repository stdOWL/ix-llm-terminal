class IXException(Exception):
    """Base exception for LLM-related errors."""
    pass


class ProviderNotReadyError(IXException):
    """Raised when the selected provider is not ready to be used."""
    pass


class InvalidProviderError(IXException):
    """Raised when the specified provider is invalid."""
    pass


class ProviderCompletionError(IXException):
    """Raised when the provider fails to generate a completion."""
    pass
