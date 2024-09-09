import math
from typing import Optional
import time
from typing import Optional, Any, List
from .interfaces.result import EvalResult, EvalResultMetric
from .utils.logger import logger
from .base_evaluator import BaseEvaluator
from datasets import Dataset
from langchain_openai.chat_models import ChatOpenAI, AzureChatOpenAI
from ragas.metrics import answer_correctness, answer_similarity
from ragas.llms import LangchainLLMWrapper
from ragas import evaluate
from .api_keys import OpenAiApiKey
from .utils.config import ConfigHelper
from .metrics.metric_type import MetricType
from datetime import datetime


class Evaluator(BaseEvaluator):
    _model: str
    _openai_api_key: Optional[str]
    _neuraltrust_failure_threshold: Optional[float] = 0.6
    
    _semantic_similarity_failure_threshold: Optional[float] = 0.6
    _correctness_failure_threshold: Optional[float] = 0.6
    

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        model: Optional[str] = None,
        evaluation_set_id: Optional[str] = None,
        testset_id: Optional[str] = None,
        next_run_at: Optional[datetime] = None,
    ):
        if model is None:
            self._model = self.default_model
        else:
            self._model = model
        
        if openai_api_key is None:
            self._openai_api_key = OpenAiApiKey.get_key()
        else:
            self._openai_api_key = openai_api_key

        self._ragas_metric = [answer_correctness, answer_similarity]
        self._evaluation_set_id = evaluation_set_id
        self._testset_id = testset_id
        self._next_run_at = next_run_at

    @property
    def display_name(self):
        return "NeuralTrust"
    
    @property
    def name(self):
        return "neuraltrust"
    
    @property
    def metric_ids(self) -> List[str]:
        return [
            MetricType.RAGAS_ANSWER_SEMANTIC_SIMILARITY.value,
            MetricType.RAGAS_ANSWER_CORRECTNESS.value,
        ]

    @property
    def default_model(self) -> str:
        return ConfigHelper.load_judge_llm_model()
    
    @property
    def ragas_metric_name(self):
        return "neuraltrust_test"

    @property
    def required_args(self):
        return ["query", "response", "expected_response"]
    
    @property
    def examples(self):
        """A list of examples for the evaluator."""
        return None

    def generate_data_to_evaluate(self, id, query, response, expected_response, metadata, **kwargs) -> dict:
        """
        Generates data for evaluation.

        :param query: user query
        :param response: llm response
        :param expected_response: expected output
        :return: A dictionary with formatted data for evaluation
        """
        data = {
            "id": [id],
            "question": [query],
            "answer": [response],
            "ground_truth": [expected_response],
            "metadata": [metadata]
        }
        return data
    
    def get_ragas_metric(self) -> List[Any]:
        return self._ragas_metric

    def set_ragas_metric(self, value: List[Any]):
        self._ragas_metric = value
    
    @property
    def grade_reason(self) -> str:
        return "Answer Semantic Similarity pertains to the assessment of the semantic resemblance between the generated response and the ground truth. This evaluation is based on the ground truth and the response, with values falling within the range of 0 to 1. A higher score signifies a better alignment between the generated response and the ground truth"
    
    def _get_model(self):
        return ChatOpenAI(model_name=self._model, api_key=self._openai_api_key)
    
    def is_failure(self, metrics) -> bool:
        if not metrics:
            return False

        threshold_mapping = {
            'answer_similarity': self._semantic_similarity_failure_threshold,
            'answer_correctness': self._correctness_failure_threshold,
        }

        all_above_threshold = True
        score_metric = None

        for metric in metrics:
            if metric['id'] == "score":
                score_metric = metric
                continue

            if metric['id'] in threshold_mapping:
                failure_threshold = threshold_mapping[metric['id']]
                if failure_threshold is not None and metric['value'] < failure_threshold:
                    return True
                all_above_threshold = all_above_threshold and (failure_threshold is None or metric['value'] >= failure_threshold)

        if all_above_threshold and score_metric and self._neuraltrust_failure_threshold is not None:
            return score_metric['value'] < self._neuraltrust_failure_threshold

        return False

    def _evaluate(self, **kwargs) -> EvalResult:
        """
        Run the Ragas evaluator.
        """
        start_time = time.time()
        self.validate_args(**kwargs)
        metrics = []
        try:
            self.set_ragas_metric([type(metric)(llm=LangchainLLMWrapper(langchain_llm=self._get_model())) for metric in self.get_ragas_metric()])
            data = self.generate_data_to_evaluate(**kwargs)
            testset = Dataset.from_dict(data)

            scores = [evaluate(testset, metrics=[metric]) for metric in self._ragas_metric]
            metrics = []
            total_score = 0
            valid_metrics_count = 0
            for score_dict in scores:
                for metric_name, metric_value in score_dict.items():
                    if isinstance(metric_value, (int, float)) and not math.isnan(metric_value):
                        metrics.append(EvalResultMetric(id=metric_name, value=metric_value))
                        total_score += metric_value
                        valid_metrics_count += 1
                    else:
                        logger.warn(f"Invalid metric value for {metric_name}: {metric_value}")

            if not metrics:
                logger.warn("No valid metrics found in the scores")
            else:
                # Calculate and add the average metric
                avg_score = total_score / valid_metrics_count
                metrics.append(EvalResultMetric(id="score", value=avg_score))
    
            failure = self.is_failure(metrics=metrics)
        except Exception as e:
            logger.error(f"Error occurred during eval: {e}")
            raise e

        end_time = time.time()
        eval_runtime_ms = int((end_time - start_time) * 1000)
        llm_eval_result = EvalResult(
            name=self.name,
            display_name=self.display_name,
            data=kwargs,
            evaluation_set_id=self._evaluation_set_id,
            testset_id=self._testset_id,
            next_run_at=self._next_run_at,
            failure=bool(failure),
            reason=self.grade_reason,
            runtime=eval_runtime_ms,
            model=self._model,
            metrics=metrics,
        )
        return {k: v for k, v in llm_eval_result.items() if v is not None}