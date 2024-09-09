import json
import requests
from jsonpath_ng import parse
import yaml
from datetime import datetime, timedelta
from sseclient import SSEClient
from ..services.api_service import NeuralTrustApiService
from ..utils.config import ConfigHelper

class APIClient:
    def __init__(self, evaluation_set_id):
        self.evaluation_set_id = evaluation_set_id
        self.api_config = yaml.safe_load(self._load_config())
        self.auth_token = None
        self.token_expiry = None

    def _load_config(self):
        local_config = ConfigHelper.load_endpoint_config()
        
        if not local_config:
            local_config = self._load_config_from_database()
        
        return local_config

    def _load_config_from_database(self):
        try:
            app_data = NeuralTrustApiService.load_api_config()
            evaluation_endpoint = app_data.get('evaluationEndpoint')
            if not evaluation_endpoint:
                raise ValueError("evaluationEndpoint is required but not found in the database.")
            return evaluation_endpoint
        except Exception as e:
            print(f"Error loading configuration from database: {e}")
            return {}

    def get_auth_token(self):
        if self.auth_token and datetime.now() < self.token_expiry:
            return self.auth_token

        try:
            response = requests.post(
                self.api_config['token_url'],
                json={
                    "user": self.api_config['username'],
                    "password": self.api_config['password']
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            self.auth_token = response.json()['token']
            self.token_expiry = datetime.now() + timedelta(hours=1)
            return self.auth_token
        except requests.RequestException as e:
            print(f"Error getting auth token: {e}")
            return None

    def run(self, test):
        headers = self._prepare_headers()
        payload = self._prepare_payload(test=test)
        try:
            response = self._make_api_request(headers, payload)
            content_type = response.headers.get('Content-Type', '')

            if 'text/event-stream' in content_type:
                return self._handle_event_stream(response)
            elif 'application/json-lines' in content_type:
                return self._handle_json_lines(response)
            else:
                return self._handle_json_response(response)
        except requests.RequestException as e:
            self._log_error(e)
            return None

    def _prepare_headers(self):
        headers = self.api_config.get('headers', {})
        if self.api_config.get('authentication', True):
            token = self.get_auth_token()
            if token:
                headers['Authorization'] = f"Bearer {token}"
        return headers

    def _prepare_payload(self, test):
        payload = self.api_config.get('payload', {})
        
        def replace_placeholders(value):
            if isinstance(value, str):
                value = value.replace('{{ test }}', test)
                value = value.replace('{{ date }}', datetime.now().strftime('%Y-%m-%d'))
                return value
            elif isinstance(value, dict):
                return {k: replace_placeholders(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_placeholders(item) for item in value]
            return value

        return replace_placeholders(payload)

    def _make_api_request(self, headers, payload):
        try:
            response = requests.post(
                self.api_config['url'],
                json=payload,
                headers=headers,
                stream=False
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self._log_error(e)
            return None

    def _handle_event_stream(self, response):
        client = SSEClient(response)
        last_json = None
        for event in client.events():
            if event.event == 'message':
                try:
                    data = json.loads(event.data)
                    last_json = data
                    print(f"Received event: {data}")
                except json.JSONDecodeError:
                    print(f"Received non-JSON event: {event.data}")
        return self._extract_field(last_json)

    def _handle_json_lines(self, response):
        full_content = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    data = json.loads(line)
                    if self._should_concatenate(data):
                        full_content += self._get_concatenate_value(data)
                except json.JSONDecodeError:
                    print(f"Received invalid JSON: {line}")
        return full_content

    def _handle_json_response(self, response):
        data = response.json()
        return self._extract_field(data)

    def _extract_field(self, data):
        if data and 'response' in self.api_config:
            field = self.api_config['response']
            jsonpath_expr = parse(field)
            matches = jsonpath_expr.find(data)
            return matches[0].value if matches else None
        return data

    def _should_concatenate(self, data):
        return ('concatenate_field' in self.api_config and
                self.get_nested_value(data, 'choices.0.messages.0.role') == 'assistant')

    def _get_concatenate_value(self, data):
        field_to_concatenate = self.api_config['concatenate_field']
        return self.get_nested_value(data, field_to_concatenate) or ''

    def _log_error(self, error):
        import traceback
        traceback.print_exc()

    def get_nested_value(self, data, field):
        keys = field.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            elif isinstance(value, list) and key.isdigit():
                index = int(key)
                if 0 <= index < len(value):
                    value = value[index]
                else:
                    return None
            else:
                return None
            if value is None:
                return None
        return str(value)