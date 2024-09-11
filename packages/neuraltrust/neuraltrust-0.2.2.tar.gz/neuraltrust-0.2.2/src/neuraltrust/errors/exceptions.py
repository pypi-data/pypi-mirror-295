from typing import Optional

class UserMessages:
    """
    Messages displayed to users.
    """

    SIGNUP_RECOMMENDATION = """
To get the most out of our service, create an account at https://neuraltrust.ai and configure your NeuralTrust API key.
"""

    MISSING_OPENAI_KEY = """
An OpenAI API key is required to continue.
    """



class CustomException(Exception):
    def __init__(
        self, message: Optional[str] = None, extra_info: Optional[dict] = None
    ):
        self.message = message
        self.extra_info = extra_info
        super().__init__(self.message)

    def __str__(self):
        if self.extra_info:
            return f"{self.message} (Extra Info: {self.extra_info})"
        return self.message


class NoNeuralTrustApiKeyException(CustomException):
    def __init__(self, message: str = UserMessages.SIGNUP_RECOMMENDATION):
        super().__init__(message)


class NoOpenAiApiKeyException(CustomException):
    def __init__(self, message: str = UserMessages.MISSING_OPENAI_KEY):
        super().__init__(message)

class ImportError(CustomException):
    def __init__(self, missing_package: str) -> None:
        super().__init__(message=f"The '{missing_package}' Python package is not installed; please execute 'pip install {missing_package}' to obtain it.")