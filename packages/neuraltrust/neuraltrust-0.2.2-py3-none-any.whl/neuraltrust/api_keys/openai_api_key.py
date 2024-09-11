from abc import ABC


class OpenAiApiKey(ABC):
    _openai_api_key = None

    @classmethod
    def set_key(cls, api_key):
        cls._openai_api_key = api_key

    @classmethod
    def get_key(cls):
        return cls._openai_api_key
    
class AzureApiKey(ABC):
    _azure_api_key = None
    _azure_base_url = None
    _azure_api_version = None

    @classmethod
    def set_key(cls, api_key):
        cls._azure_api_key = api_key

    @classmethod
    def get_key(cls):
        return cls._azure_api_key

    @classmethod
    def set_base_url(cls, base_url):
        cls._azure_base_url = base_url

    @classmethod
    def get_base_url(cls):
        return cls._azure_base_url
    
    @classmethod
    def set_api_version(cls, api_version):
        cls._azure_api_version = api_version

    @classmethod
    def get_api_version(cls):
        return cls._azure_api_version