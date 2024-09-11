import requests
from typing import List, Optional, Dict
from ..api_keys import NeuralTrustApiKey
from ..utils.constants import API_BASE_URL
from ..errors.exceptions import CustomException

#SDK_VERSION = pkg_resources.get_distribution("neuraltrust").version

class NeuralTrustApiService:
    @staticmethod
    def _headers():
        neuraltrust_api_key = NeuralTrustApiKey.get_key()
        return {
            "token": neuraltrust_api_key,
        }

    
    @staticmethod
    def firewall(input: str):
        """
        Invokes the firewall endpoint to check the input text.

        Parameters:
        - text (str): The input text to be checked.

        Returns:
        The API response data for the firewall check.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/firewall"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json={"input": input},
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get('details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            raise

    @staticmethod
    def create_testset(
        testset: List[Dict]
    ):
        """
        Creates a testset by calling the NeuralTrust API
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/testset"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=testset,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise
    
    @staticmethod
    def update_testset(
        testset_id: str,
        update_data: Dict
    ):
        """
        Updates a testset by calling the NeuralTrust API.

        Parameters:
        - testset_id (str): The ID of the testset to update.
        - update_data (Dict): A dictionary containing the data to update in the testset.

        Returns:
        The API response data for the updated testset.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/testset/{testset_id}"
            response = requests.put(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=update_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise
    
    @staticmethod
    def create_evaluation_set(evaluation_set_data: Dict):
        """
        Creates a new evaluation set by calling the NeuralTrust API.

        Parameters:
        - evaluation_set_data (Dict): A dictionary containing the data for the new evaluation set.

        Returns:
        The API response data for the created evaluation set.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-set"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=evaluation_set_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise

    @staticmethod
    def update_evaluation_set(evaluation_set_id: str, update_data: Dict):
        """
        Updates an existing evaluation set by calling the NeuralTrust API.

        Parameters:
        - evaluation_set_id (str): The ID of the evaluation set to update.
        - update_data (Dict): A dictionary containing the data to update in the evaluation set.

        Returns:
        The API response data for the updated evaluation set.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-set/{evaluation_set_id}"
            response = requests.put(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=update_data,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise
    
    @staticmethod
    def load_evaluation_set(evaluation_set_id: str):
        """
        Loads an existing evaluation set by calling the NeuralTrust API.

        Parameters:
        - evaluation_set_id (str): The ID of the evaluation set to load.

        Returns:
        The API response data for the loaded evaluation set.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-set/{evaluation_set_id}"
            response = requests.get(
                endpoint,
                headers=NeuralTrustApiService._headers(),
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise
        
    @staticmethod
    def load_api_config():
        """
        Loads an existing evaluation set by calling the NeuralTrust API.

        Parameters:
        - evaluation_set_id (str): The ID of the evaluation set to load.

        Returns:
        The API response data for the loaded evaluation set.

        Raises:
        - CustomException: If the API call fails or returns an error.
        """
        try:
            endpoint = f"{API_BASE_URL}/v1/app"
            response = requests.get(
                endpoint,
                headers=NeuralTrustApiService._headers(),
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise

    @staticmethod
    def fetch_testset_rows(
        testset_id: str,
        number_of_rows: Optional[int] = None
    ):
        """
        Fetch the testset rows by calling the NeuralTrust API

        """
        try:
            if number_of_rows is None:
                number_of_rows = 500
            endpoint = f"{API_BASE_URL}/v1/testset/fetch-by-id/{testset_id}?offset=0&limit={number_of_rows}"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers()
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()['data']
        except Exception as e:
            raise

    @staticmethod
    def log_eval_details(eval_results: dict):
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-run/details"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=eval_results,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
    
    def log_eval_run(eval_run: dict):
        try:
            endpoint = f"{API_BASE_URL}/v1/evaluation-run"
            response = requests.post(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=eval_run,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise

    def update_testsets(testsets: List[Dict]):
        try:
            endpoint = f"{API_BASE_URL}/v1/testset"
            response = requests.put(
                endpoint,
                headers=NeuralTrustApiService._headers(),
                json=testsets,
            )
            if response.status_code == 401:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = 'please check your neuraltrust api key and try again'
                raise CustomException(error_message, details_message)
            elif response.status_code != 200 and response.status_code != 201:
                response_json = response.json()
                error_message = response_json.get('error', 'Unknown Error')
                details_message = response_json.get(
                    'details', {}).get('message', 'No Details')
                raise CustomException(error_message, details_message)
            return response.json()
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise
