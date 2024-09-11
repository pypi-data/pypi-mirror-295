from enum import Enum

class RagasEvalTypeId(Enum):
    RAGAS_CONTEXT_RELEVANCY = "RagasContextRelevancy"
    RAGAS_ANSWER_RELEVANCY = "RagasAnswerRelevancy"
    RAGAS_CONTEXT_PRECISION = "RagasContextPrecision"
    RAGAS_FAITHFULNESS = "RagasFaithfulness"
    RAGAS_CONTEXT_RECALL = "RagasContextRecall"
    RAGAS_ANSWER_SEMANTIC_SIMILARITY = "RagasAnswerSemanticSimilarity"
    RAGAS_ANSWER_CORRECTNESS = "RagasAnswerCorrectness"
    RAGAS_HARMFULNESS = "RagasHarmfulness"
    RAGAS_MALICIOUSNESS = "RagasMaliciousness"
    RAGAS_COHERENCE = "RagasCoherence"
    RAGAS_CONCISENESS = "RagasConciseness"


class GroundedEvalTypeId(Enum):
    ANSWER_SIMILARITY = "AnswerSimilarity"
    CONTEXT_SIMILARITY = "ContextSimilarity"

def is_ragas_eval(evaluator_type: str) -> bool:
    return any(evaluator_type == member.value for member in RagasEvalTypeId)

def is_grounded_eval(evaluator_type: str) -> bool:
    return any(evaluator_type == member.value for member in GroundedEvalTypeId)

