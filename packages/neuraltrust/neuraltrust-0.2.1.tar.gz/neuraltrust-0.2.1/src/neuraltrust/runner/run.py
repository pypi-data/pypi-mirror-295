from typing import List, TypedDict, Optional
from testset.testset import Testset
from neuraltrust.base_evaluator import BaseEvaluator
from utils.dataset_helper import generate_unique_dataset_name
from interfaces.result import EvalResult
from interfaces.data import DataPoint
import pandas as pd
import json
import hashlib


class LlmBatchEvalResult(TypedDict):
    """Result of running a batch of LLM evaluations."""

    results: List[EvalResult]
    total_runtime: float
    passed_evals: int
    failed_evals: int
    total_evals: int
    total_datapoints: int


class EvalRunner:
    @staticmethod
    def flatten_eval_results(batch_eval_results) -> List:
        # Flatten the list of lists into a single list of evaluation results
        flattened_results = [
            item
            for sublist in batch_eval_results
            for item in (sublist if sublist is not None else [None])
        ]
        return flattened_results

    @staticmethod
    def to_df(batch_eval_results):
        # Initialize a dictionary to hold the aggregated data
        aggregated_data = {}

        flattened_results = EvalRunner.flatten_eval_results(
            batch_eval_results=batch_eval_results
        )
        # Process each evaluation result
        for eval_result in flattened_results:
            if eval_result is not None:
                # Serialize and hash the datapoint dictionary to create a unique identifier
                datapoint_hash = hashlib.md5(
                    json.dumps(eval_result["data"], sort_keys=True).encode()
                ).hexdigest()

                # Initialize the datapoint in the aggregated data if not already present
                if datapoint_hash not in aggregated_data:
                    aggregated_data[datapoint_hash] = eval_result[
                        "data"
                    ]  # Include datapoint details

                # Update the aggregated data with metrics from this evaluation
                for metric in eval_result["metrics"]:
                    metric_name = metric["id"]
                    metric_value = metric["value"]
                    aggregated_data[datapoint_hash][
                        eval_result["display_name"] + " " + metric_name
                    ] = metric_value

        # Convert the aggregated data into a DataFrame
        df = pd.DataFrame(list(aggregated_data.values()))

        return df

    @staticmethod
    def _log_eval_results(
        eval_results: List[dict], eval: BaseEvaluator, dataset_id: str
    ):
        try:
            pass
        except Exception as e:
            print(
                f"An error occurred while posting eval results",
                str(e),
            )
            raise

    @staticmethod
    def _log_testset_to_neuraltrust(data: List[DataPoint]) -> Optional[str]:
        """
        Logs the testset to NeuralTrust
        """
        try:
            dataset = Testset.create(name=generate_unique_dataset_name(), rows=data)
            return dataset
        except Exception as e:
            print(f"Error logging dataset to NeuralTrust: {e}")
            return None

    @staticmethod
    def _fetch_testset_rows(testset_id: str, number_of_rows: Optional[int] = None) -> List[any]:
        """
        Fetch the testset rows from NeuralTrust
        """
        try:
            rows = Testset.fetch_testset_rows(testset_id=testset_id, number_of_rows=number_of_rows)
            return rows
        except Exception as e:
            print(f"Error fetching testset rows: {e}")
            return None

    @staticmethod
    def run_suite(
        evals: List[BaseEvaluator],
        data: List[DataPoint] = None,
        max_parallel_evals: int = 5,
        testset_id: Optional[str] = None,
        number_of_rows: Optional[int] = None,
    ) -> List[LlmBatchEvalResult]:
        """
        Run a suite of LLM evaluations against a dataset.

        Args:
            evals: A list of LlmEvaluator objects.
            data: A list of data points.

        Returns:
            A list of LlmBatchEvalResult objects.
        """
        if data:
            # Log T to NeuralTrust
            testset = EvalRunner._log_testset_to_neuraltrust(data)
            testset_id = testset.id
        elif testset_id is not None:
            testset = EvalRunner._fetch_testset_rows(testset_id, number_of_rows)
            data = testset
        else:
            raise Exception("No data or testset_id provided.")  

        batch_results = []
        for eval in evals:
            # Run the evaluations
            if max_parallel_evals > 1:
                eval_results = eval._run_batch_generator_async(data, max_parallel_evals)
            else:
                eval_results = list(eval._run_batch_generator(data))

            if testset:
                EvalRunner._log_eval_results_with_config(
                    eval_results=eval_results, eval=eval, testset_id=testset_id
                )
            batch_results.append(eval_results)

        if testset:
            print(f"You can view your testset at: {Testset.testset_link(testset_id)}")

        return EvalRunner.to_df(batch_results)
