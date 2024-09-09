from .base import ChatMessage, LLMClient
from .logger import LLMLogger
from ...utils.config import ConfigHelper
from ...api_keys import AzureApiKey, OpenAiApiKey

_target_client = None
_judge_client = None

def set_target_client(client: LLMClient):
    global _target_client
    _target_client = client

def set_judge_client(client: LLMClient):
    global _judge_client
    _judge_client = client


def get_judge_client() -> LLMClient:
    global _judge_client

    if _judge_client is not None:
        return _judge_client

    from .openai import OpenAIClient

    default_llm_api = ConfigHelper.load_judge_llm_provider()
    default_judge_llm_model = ConfigHelper.load_judge_llm_model()

    try:
        from openai import AzureOpenAI, OpenAI
        client = AzureOpenAI(base_url=AzureApiKey.get_base_url(), api_version=AzureApiKey.get_api_version(), api_key=AzureApiKey.get_key()) if default_llm_api == "azure" else OpenAI(api_key=OpenAiApiKey.get_key())

        _judge_client = OpenAIClient(model=default_judge_llm_model, client=client)
    except ImportError:
        raise ValueError(f"LLM scan using {default_llm_api.name} require openai>=1.0.0")

    return _judge_client



def get_target_client() -> LLMClient:
    global _target_client

    if _target_client is not None:
        return _target_client

    from .openai import OpenAIClient

    default_llm_api = ConfigHelper.load_target_llm_provider()
    default_target_llm_model = ConfigHelper.load_target_llm_model()

    try:
        from openai import AzureOpenAI, OpenAI
        client = AzureOpenAI(
            base_url='https://neuraltrust.openai.azure.com/',
            azure_deployment=default_target_llm_model,
            api_key=AzureApiKey.get_key(),
            api_version="2024-05-01-preview"
        ) if default_llm_api == "azure" else OpenAI()

        _target_client = OpenAIClient(model=default_target_llm_model, client=client)
    except ImportError:
        raise ValueError(f"LLM scan using {default_llm_api.name} require openai>=1.0.0")

    return _target_client


__all__ = [
    "LLMClient",
    "ChatMessage",
    "LLMLogger",
    "get_target_client",
    "set_target_client",
    "get_judge_client",
    "set_judge_client",
]
