import time
import inspect
from typing import Dict
import neuraltrust
from ..errors.exceptions import NoOpenAiApiKeyException
from ..interfaces.model import Model
from ..utils.config import ConfigHelper
from ..evaluator import Evaluator
from ..interfaces.data import DataPoint
from ..testset import Testset
from ..api_keys import OpenAiApiKey, NeuralTrustApiKey
from ..services.api_service import NeuralTrustApiService
from ..target import complete
from ..llm.client import ChatMessage
import json

class RunHelper:
    @staticmethod
    def all_evals():
        # List to store the names of classes
        exported_classes = []

        # Iterate through each attribute in the module
        for name in dir(neuraltrust):
            # Get the attribute
            attribute = getattr(neuraltrust, name)

            # Check if the attribute is a class and is listed in __all__
            if inspect.isclass(attribute) and name in neuraltrust.__all__:
                exported_classes.append(name)

        # Return the names of the exported classes
        return exported_classes

    @staticmethod
    def get_evaluator(eval_id, **kwargs):
        """Returns an evaluator class based on the eval name"""

        # Retrieve the evaluation class based on eval_id
        eval_class = getattr(neuraltrust, eval_id, None)

        # Check if the eval class exists and is a class
        if eval_class is None or not inspect.isclass(eval_class):
            raise ValueError(f"Invalid evaluation name: {eval_id}")

        return eval_class(**kwargs)

    @staticmethod
    def validate_eval_args(eval_id, model, kwargs):
        """Validates the arguments for an eval"""

        # Check if eval_id is a valid eval
        available_evals = RunHelper.all_evals()
        if eval_id not in available_evals:
            raise ValueError(
                f"{eval_id} is not a valid eval.\n\nUse `neuraltrust list` to see all available evals."
            )

        # Check if model is in supported models
        if not Model.is_supported(model):
            raise ValueError(
                f"{model} is not a valid model.\n\nUse `neuraltrust models` to see all available models."
            )

        # Retrieve the evaluation class based on eval_id
        evaluator = RunHelper.get_evaluator(eval_id, model=model)

        # Check if the eval class exists
        if evaluator is None:
            raise ValueError(f"Invalid evaluation name: {eval_id}")

        # Retrieve the required arguments from the eval class
        required_args = evaluator.required_args

        # Check if each required argument is in kwargs
        missing_args = [arg for arg in required_args if arg not in kwargs]
        if missing_args:
            raise ValueError(
                f"Missing required arguments for {eval_id}: {', '.join(missing_args)}"
            )

        # If all required arguments are present, return True or some confirmation
        return True

    @staticmethod
    def _set_keys():
        openai_api_key = ConfigHelper.load_openai_api_key()
        if (openai_api_key is None):
            raise NoOpenAiApiKeyException
        OpenAiApiKey.set_key(openai_api_key)

        neuraltrust_api_key = ConfigHelper.load_neuraltrust_api_key()
        NeuralTrustApiKey.set_key(neuraltrust_api_key)

    @staticmethod
    def run_eval(eval_id, testset_id, model, **kwargs):
        """Runs an eval and returns the results"""

        print(f"Running eval {eval_id} on {model}...\n")
        # Set the keys globally
        RunHelper._set_keys()

        # Validate the arguments for the eval
        # if not RunHelper.validate_eval_args(eval_id, model, kwargs):
        #     # Handle invalid arguments, either by raising an exception or returning an error
        #     raise ValueError("Invalid arguments for the evaluation.")

        # Run the evaluation
        dataset = [kwargs]
        return RunHelper.run_eval_on_dataset(eval_id, testset_id, model, dataset, max_parallel_evals=5)

    @staticmethod
    def _load_existing_evaluation_set(id):
        evalset_data = NeuralTrustApiService.load_evaluation_set(id)
        testset_id = evalset_data.get("testsetId", None)
        return testset_id
        

    @staticmethod
    def _load_testset_from_neuraltrust(testset_id: str):
        try:
            return Testset.fetch_testset_rows(
                testset_id=testset_id,
                number_of_rows=20
            )
        except Exception as e:
            raise ValueError(f"Failed to load testset to NeuralTrust: {e}")
        
    @staticmethod
    def _update(id: str, eval_set: Dict):
        """
        Updates an existing evaluation set with the specified properties.
        Raises:
        - Exception: If the testset could not be updated due to an error like invalid parameters, database errors, etc.
        """
        try:
            NeuralTrustApiService.update_evaluation_set(id, eval_set)
        except Exception as e:
            raise

    @staticmethod
    def run_eval_on_batch(eval_id, model, max_parallel_evals=5, **kwargs):
        """Runs an eval on a batch dataset and outputs results in a user-friendly format"""

        print(f"Running eval {eval_id} on {model}...")
        # Set the keys globally
        RunHelper._set_keys()
        testset_id = RunHelper._load_existing_evaluation_set(eval_id)
        RunHelper._update(eval_id, {'testsetId': testset_id})
        remote_data = RunHelper._load_testset_from_neuraltrust(testset_id)

        if not remote_data:
            raise ValueError(f"No data found for testset_id: {testset_id}")
        dataset = [DataPoint(**row) for row in remote_data]
        
        RunHelper._update(eval_id, {'testsetId': testset_id})

        return RunHelper.run_eval_on_dataset(eval_id, testset_id, model, dataset, max_parallel_evals)

    def _run_target(data: DataPoint) -> DataPoint:
        context = data['context'] + "\n"+ data['query']
        conversation_history = []
        if data['conversation_history'] is not None and data['conversation_history'] != "{}":
            conversation_history = [ChatMessage(**json.loads(msg)) if isinstance(msg, str) else ChatMessage(role=msg.get('role', ''), content=msg.get('content', '')) for msg in data['conversation_history']]
        response = complete({"system_prompt": ""}, context, conversation_history)

        if response.content is None:
            raise ValueError("No content in response")
        data['response'] = response.content
        return data
    
    @staticmethod
    def run_eval_on_dataset(eval_id, testset_id, model, dataset, max_parallel_evals, **kwargs):
        # Retrieve evaluator
        evaluator = Evaluator(evaluation_set_id=eval_id, testset_id=testset_id, neuraltrust_failure_threshold=0.7)
        data = [RunHelper._run_target(data) for data in dataset]

        # Run batch evaluation and measure time
        start = time.perf_counter()
        result = evaluator.run_batch( data=data, max_parallel_evals=max_parallel_evals)
        end = time.perf_counter()
        runtime = end - start

        # Output formatting
        print(f"\nEvaluation: {eval_id}")
        print(f"Model: {model}")
        print(f"Runtime: {runtime // 60} minutes and {runtime % 60:.2f} seconds\n")

        # Error handling and output
        print("\nResults:")
        for eval_result in result.eval_results:
            pass_fail_text = "❌ FAILED" if eval_result["failure"] else "✅ PASSED"
            
            # Printing data with structured formatting
            print(f"\n{'————' * 8}")
            print(f"\nData: {eval_result['data']}\n")
            print(f"{pass_fail_text}\n")
            print(f"Reason: {eval_result['reason']}\n")
            print(f"Metrics: {eval_result['metrics']}")

        return result