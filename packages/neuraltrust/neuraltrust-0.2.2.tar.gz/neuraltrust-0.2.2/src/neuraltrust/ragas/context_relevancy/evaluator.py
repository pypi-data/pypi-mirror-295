from ...interfaces.model import Model
from ...ragas.ragas_evaluator import RagasEvaluator
from ...eval_type import RagasEvalTypeId
from ...metrics.metric_type import MetricType
from typing import List, Optional
from ragas.metrics import context_precision

"""
RAGAS Context Relevancy Docs: https://docs.ragas.io/en/latest/concepts/metrics/context_relevancy.html
RAGAS Context Relevancy Github: https://github.com/explodinggradients/ragas/blob/main/src/ragas/metrics/_context_relevancy.py
"""
class RagasContextRelevancy(RagasEvaluator):
    """
    This evaluator calculates the relevancy of the context with respect to the user query.
    """
    @property
    def name(self):
        return RagasEvalTypeId.RAGAS_CONTEXT_RELEVANCY.value

    @property
    def display_name(self):
        return "Ragas Context Relevancy"

    @property
    def metric_ids(self) -> List[str]:
        return [MetricType.RAGAS_CONTEXT_RELEVANCY.value]
    
    @property
    def ragas_metric(self):
        return context_precision
    
    @property
    def ragas_metric_name(self):
        return "ragas_context_relevancy"

    @property
    def default_model(self):
        return Model.GPT35_TURBO.value

    @property
    def required_args(self):
        return ["id", "query", "context"]

    @property
    def examples(self):
        return None
    
    @property
    def grade_reason(self) -> str:
        return "This metric is calulated by dividing the number of sentences in context that are relevant for answering the given query by the total number of sentences in the retrieved context"

    def is_failure(self, score) -> Optional[bool]:
        return bool(score < self._failure_threshold) if self._failure_threshold is not None else None
        
    def generate_data_to_evaluate(self, id, context, query, **kwargs) -> dict:
        """
        Generates data for evaluation.

        :param context: list of strings of retrieved context
        :param query: user query
        :return: A dictionary with formatted data for evaluation
        """
        data = {
            "id": id,
            "contexts": [context],
            "question": [query]
        }
        return data
