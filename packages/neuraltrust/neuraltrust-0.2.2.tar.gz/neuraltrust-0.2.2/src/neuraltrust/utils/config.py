import yaml
import os

CONFIG_FILE_NAME = "config.yml"


class ConfigHelper:
    @staticmethod
    def load_config():
        try:
            with open(CONFIG_FILE_NAME, "r") as file:
                config = yaml.safe_load(file)

            if config is None:
                config = {}
            return config
        except:
            return {}

    @staticmethod
    def load_config_field(field: str):
        try:
            config = ConfigHelper.load_config()
            return config[field]
        except Exception as e:
            return None

    @staticmethod
    def load_endpoint_config():
        return ConfigHelper.load_config_field("endpoint_config") or os.getenv("ENDPOINT_CONFIG")
    
    @staticmethod
    def load_openai_api_key():
        return ConfigHelper.load_config_field("openai_api_key") or os.getenv("OPENAI_API_KEY")

    @staticmethod
    def load_azure_api_key():
        return ConfigHelper.load_config_field("azure_api_key") or os.getenv("AZURE_API_KEY")
    
    @staticmethod
    def load_neuraltrust_api_key():
        return ConfigHelper.load_config_field("neuraltrust_api_key") or os.getenv("NEURALTRUST_API_KEY")

    @staticmethod
    def load_judge_llm_model():
        return ConfigHelper.load_config_field("judge_llm_model") or os.getenv("JUDGE_LLM_MODEL") or "gpt-4o-mini"

    @staticmethod
    def load_target_llm_model():
        return ConfigHelper.load_config_field("target_llm_model") or os.getenv("TARGET_LLM_MODEL") or "gpt-4o-mini"

    @staticmethod
    def load_judge_llm_provider():
        return ConfigHelper.load_config_field("judge_llm_provider") or os.getenv("JUDGE_LLM_PROVIDER") or "openai"

    @staticmethod
    def load_target_llm_provider():
        return ConfigHelper.load_config_field("target_llm_provider") or os.getenv("TARGET_LLM_PROVIDER") or "openai"

    @staticmethod
    def save_config(config_data):
        with open(CONFIG_FILE_NAME, "w") as file:
            yaml.dump(config_data, file)

    @staticmethod
    def is_set():
        try:
            with open(CONFIG_FILE_NAME, "r") as file:
                config = yaml.safe_load(file)

            if config is None or config == {}:
                return False
            else:
                return True
        except:
            return False
