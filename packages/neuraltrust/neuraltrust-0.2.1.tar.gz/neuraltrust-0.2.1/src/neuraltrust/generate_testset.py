from typing import List, Dict
from .interfaces.data import DataPoint
from .generators import generate_testset, KnowledgeBase
from .utils import _generate_id
from .testset import Testset
from .services.api_service import NeuralTrustApiService
import pandas as pd


class GenerateTestset:
    def __init__(self,
                 evaluation_set_id: str = None,
                 num_questions: int = 10,
                 knowledge_base: KnowledgeBase = None):

        self.evaluation_set_id = evaluation_set_id
        self.name = None
        self.description = None
        self.num_questions = num_questions
        self.knowledge_base = knowledge_base

        self._load_existing_evaluation_set()

    def _load_existing_evaluation_set(self):
        evalset_data = NeuralTrustApiService.load_evaluation_set(self.evaluation_set_id)
        self.name = evalset_data.get("name")
        self.description = evalset_data.get("description")

    def _load_testset_to_neuraltrust(self, testset_id: str, data: List[DataPoint]):
        try:
            Testset.create(
                id=self.evaluation_set_id,
                testset_id=testset_id,
                rows=data
            )
        except Exception as e:
            raise ValueError(f"Failed to load testset to NeuralTrust: {e}")

    def _update(self, eval_set: Dict):
        """
        Updates an existing evaluation set with the specified properties.
        Raises:
        - Exception: If the testset could not be updated due to an error like invalid parameters, database errors, etc.
        """
        try:
            NeuralTrustApiService.update_evaluation_set(self.evaluation_set_id, eval_set)
        except Exception as e:
            raise

    def _generate_testset(self, knowledge_base: pd.DataFrame, num_questions: int, description: str) -> str:
        if self.knowledge_base is None:
            raise ValueError("Knowledge base is not set.")

        testset_id = _generate_id(f"{self.name}_testset")

        testset = generate_testset(
            knowledge_base,
            num_questions=num_questions,
            agent_description=description,
        )

        testset.save(path=f"/tmp/{testset_id}.json")
        self._load_testset_to_neuraltrust(testset_id, testset.samples)
        self._update({'testsetId': testset_id})
        return testset_id

    def generate(self):
        return self._generate_testset(self.knowledge_base, self.num_questions, self.description)
