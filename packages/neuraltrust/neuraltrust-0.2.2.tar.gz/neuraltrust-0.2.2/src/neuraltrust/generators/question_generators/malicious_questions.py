from .. import KnowledgeBase
from ..testset import QuestionSample
from .base import _BaseModifierGenerator
from .simple_questions import SimpleQuestionsGenerator


class MaliciousQuestionGenerator(_BaseModifierGenerator):
    _base_generator = SimpleQuestionsGenerator()

    def _modify_question(self, question: QuestionSample, knowledge_base: KnowledgeBase, agent_description: str, language: str) -> QuestionSample:
        messages = self._prompt.to_messages(
            system_prompt_input={
                "agent_description": agent_description,
                "language": language,
            },
            user_input={"question": question.query,
                        "context": question.context,
                        },
        )
        question.metadata["question_type"] = self._question_type
        out = self._llm_complete(messages=messages)
        question.query = out["question"]
        return question
