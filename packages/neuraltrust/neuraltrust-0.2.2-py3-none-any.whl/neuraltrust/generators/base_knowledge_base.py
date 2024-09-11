from abc import ABC, abstractmethod
from typing import Sequence

class BaseKnowledgeBase(ABC):
    @abstractmethod
    def get_random_document(self):
        pass

    @abstractmethod
    def get_neighbors(self, seed_document, n_neighbors: int = 4, similarity_threshold: float = 0.2):
        pass

    @abstractmethod
    def similarity_search_with_score(self, query: str, k: int) -> Sequence:
        pass

    @property
    @abstractmethod
    def topics(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, doc_id: str):
        pass
