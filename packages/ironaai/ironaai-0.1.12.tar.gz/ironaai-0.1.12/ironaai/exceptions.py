class UnsupportedLLMProvider(Exception):
    """The exception class for unsupported LLM provider"""


class InvalidApiKey(Exception):
    """The exception class for InvalidApiKey"""


class MissingApiKey(Exception):
    """The exception class for MissingApiKey"""


class MissingLLMConfigs(Exception):
    """The exception class for empty LLM provider configs array"""


class ApiError(Exception):
    """The exception class for any ApiError"""


class CreateUnavailableError(Exception):
    """The exception class raised when `ironaai[create]` is not available"""
