from abc import ABC


class NeuralTrustApiKey(ABC):
    _neuraltrust_api_key = None

    @classmethod
    def set_key(cls, api_key):
        cls._neuraltrust_api_key = api_key

    @classmethod
    def get_key(cls):
        return cls._neuraltrust_api_key

    @classmethod
    def is_set(cls):
        return cls._neuraltrust_api_key is not None