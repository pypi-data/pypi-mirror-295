from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Dict
from .utils.logger import logger
from .services.api_service import NeuralTrustApiService
from .utils.dataset_helper import generate_unique_dataset_name
from .interfaces.data import DataPoint
from .interfaces.result import BatchRunResult, EvalResult
from .testset import Testset
import traceback
from tabulate import tabulate
from .utils import _generate_id
import time
from datetime import datetime

class BaseEvaluator(ABC):
    
    # Abstract properties
    @property
    @abstractmethod
    def name(self) -> str:
        """A unique name identifier for the evaluator."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """A display name for the evaluator."""
        pass

    @property
    @abstractmethod
    def metric_ids(self) -> List[str]:
        """The metric computed by the evaluator."""
        pass

    @property
    @abstractmethod
    def required_args(self) -> List[str]:
        """A list of required arguments for the evaluator."""
        pass

    @property
    @abstractmethod
    def examples(self):
        """A list of examples for the evaluator."""
        pass

    @abstractmethod
    def is_failure(self, *args) -> Optional[bool]:
        """A method to determine if the evaluation failed."""
        pass

    @abstractmethod
    def _evaluate(self, **kwargs) -> EvalResult:
        """The method that performs the evaluation."""
        pass
    
    def to_config(self) -> Optional[Dict]:
        return None

    # Common methods
    def _examples_str(self) -> str:
        return "" if self.examples is None else "\n".join(map(str, self.examples))


    def validate_args(self, **kwargs) -> None:
        """
        Validates that all required arguments are present and not None.
        """
        for arg in self.required_args:
            if arg not in kwargs:
                raise ValueError(f"Missing required argument: {arg}")
            elif kwargs[arg] is None:
                raise ValueError(f"{arg} cannot be None")

    def _validate_batch_args(self, data: List[DataPoint]) -> bool:
        """
        Validates that each entry in the batch has all the required arguments,
        and none of the arguments is None.
        """
        for i, entry in enumerate(data):
            for arg in self.required_args:
                if arg not in entry:
                    raise ValueError(
                        f"Data at index {i} is missing required argument: {arg}"
                    )
                elif entry[arg] is None:
                    raise ValueError(
                        f"Data at index {i} has required argument {arg} set to None"
                    )
        return True

    def _run_batch_generator_async(
        self, data: List[DataPoint], max_parallel_evals: int
    ):
        with ThreadPoolExecutor(max_workers=max_parallel_evals) as executor:
            # Submit all tasks to the executor and store them with their original index
            future_to_index = {
                executor.submit(self._evaluate, **entry): i
                for i, entry in enumerate(data)
            }

            # Create a list to store results in the original order
            results = [None] * len(data)

            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    results[index] = future.result()
                except Exception as e:
                    entry = data[index]
                    logger.error(f"Error running batch async {entry}: {e}")
                    traceback.print_exc()
                    results[index] = None

            return results

    def _run_batch_generator(self, data: List[DataPoint]):
        """
        Generator function for running a batch of evaluations.
        Iterates over a dataset, and runs the evaluator on each entry.
        """
        for entry in data:
            try:
                yield self._evaluate(**entry)
            except Exception as e:
                logger.error(f"Error evaluating entry {entry}: {e}")
                traceback.print_exc()
                yield None

    def _log_testset_to_neuraltrust(self, data: List[DataPoint]) -> Optional[str]:
        """
        Logs the testset to NeuralTrust
        """
        try: 
            dataset = Testset.update(
                name=generate_unique_dataset_name(),
                rows=data
            )
            return dataset
        except Exception as e:
            print(f"Error logging dataset to NeuralTrust: {e}")
            return None
    
    def run_batch(
        self, data: List[DataPoint], max_parallel_evals: int = 5
    ) -> BatchRunResult:
        """
        Runs the evaluator on a batch of data.
        """

        # Run the evaluations
        if max_parallel_evals > 1:
            eval_results = self._run_batch_generator_async(data, max_parallel_evals)
        else:
            eval_results = list(self._run_batch_generator(data))
        
        self.print_eval_results(eval_results)
        self._log_eval_results_to_neuraltrust(eval_results)

        return BatchRunResult(
            eval_results=eval_results,
        )

    def _log_eval_results_to_neuraltrust(self, eval_results: List[EvalResult]):
        """
        Logs the batch results to NeuralTrust
        """
        try:
            run_data = self._prepare_run_data(eval_results)
            self._log_data_to_neuraltrust(run_data)
        except Exception as e:
            print(f"Error logging eval results to NeuralTrust: {e}")

    def _prepare_run_data(self, eval_results: List[EvalResult]):
        try:
            run_id = _generate_id(f"run_{int(time.time())}")
            evaluation_set_id = eval_results[0]['evaluation_set_id']
            now = datetime.utcnow().isoformat()
            
            details, testsets = [], []
            num_failed, num_passed = 0, 0

            for result in eval_results:
                testset = self._create_testset(result, now)
                testsets.append(testset)
                
                detail = self._create_detail(result, run_id, now)
                details.append(detail)
                
                num_failed += result['failure']
                num_passed += not result['failure']

            run = self._create_run(run_id, evaluation_set_id, eval_results, num_failed, num_passed, now)
            eval_set = self._create_eval_set(eval_results, num_failed, num_passed, now)

            return {
                'run': run,
                'eval_set': eval_set,
                'details': details,
                'testsets': testsets,
                    'evaluation_set_id': evaluation_set_id
                }
        except Exception as e:
            print(f"Error preparing run data: {e}")
            traceback.print_exc()
            return None

    def _create_testset(self, result, now):
        return {
            'id': result['data']['id'],
            'lastRun': result['failure'],
            'lastRunAt': now,
        }

    def _create_detail(self, result, run_id, now):
        data = result['data']
        return {
            'id': _generate_id(f"details_run_{int(time.time())}"),
            'evaluationRunId': run_id,
            'queryId': data['id'],
            'query': data['query'],
            'runAt': now,
            'response': data['response'],
            'expectedResponse': data['expected_response'],
            'type': data['metadata']['question_type'] if data.get('metadata') is not None and data['metadata'].get('question_type') is not None else (data.get('type') if data.get('type') is not None else None),
            'context': data['context'],
            'failure': result['failure'],
            'runtime': result['runtime'],
            'evaluationSetId': result['evaluation_set_id'],
            'testsetId': result['testset_id']
        }

    def _create_run(self, run_id, evaluation_set_id, eval_results, num_failed, num_passed, now):
        return {
            'id': run_id,
            'runAt': now,
            'evaluationSetId': evaluation_set_id,
            'testsetId': eval_results[0]['testset_id'],
            'numTests': len(eval_results),
            'numFailed': num_failed,
            'numPassed': num_passed,
            'avgPassed': num_passed / len(eval_results),
        }

    def _create_eval_set(self, eval_results, num_failed, num_passed, now):
        return {
            'lastRunAt': now,
            'nextRunAt': eval_results[0]['next_run_at'] if 'next_run_at' in eval_results[0] else None,
            'status': 'completed',
            'testsetId': eval_results[0]['testset_id'],
            'numQuestions': len(eval_results),
            'numTests': len(eval_results),
            'numFailed': num_failed,
            'numPassed': num_passed,
            'avgPassed': num_passed / len(eval_results),
        }

    def _log_data_to_neuraltrust(self, run_data):
        self._safe_api_call(NeuralTrustApiService.log_eval_run, run_data['run'])
        self._safe_api_call(NeuralTrustApiService.log_eval_details, run_data['details'])
        self._safe_api_call(NeuralTrustApiService.update_testsets, run_data['testsets'])
        self._safe_api_call(NeuralTrustApiService.update_evaluation_set, run_data['evaluation_set_id'], run_data['eval_set'])

    def _safe_api_call(self, api_function, *args):
        try:
            api_function(*args)
        except Exception as e:
            print(f"Error calling {api_function.__name__}: {e}")

    def print_eval_results(self, eval_results):
        table_data = []
        headers = ["Query", "Response", "Expected Response", "Failure", "Score"]

        for result in eval_results:
            data = result['data']
            metrics = {metric['id']: metric['value'] for metric in result['metrics']}
            score = metrics.get('score', 'N/A')
            
            table_data.append([
                data['query'][:50] + "..." if len(data['query']) > 50 else data['query'],
                data['response'][:50] + "..." if len(data['response']) > 50 else data['response'],
                data['expected_response'][:50] + "..." if len(data['expected_response']) > 50 else data['expected_response'],
                'Yes' if result['failure'] else 'No',
                f"{score:.4f}" if isinstance(score, float) else score
            ])

        print(tabulate(table_data, headers=headers, tablefmt="grid"))