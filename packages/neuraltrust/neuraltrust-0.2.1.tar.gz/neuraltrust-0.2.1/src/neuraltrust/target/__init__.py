from typing import List
from ..generators.question_generators.prompt import QAGenerationPrompt
from ..llm.client import ChatMessage, get_target_client

QA_SYSTEM_PROMPT = """
    {system_prompt}
"""

def complete(system_prompt: str, context_str: str, conversation_history: List[ChatMessage]):
    _prompt = QAGenerationPrompt(
        system_prompt=QA_SYSTEM_PROMPT
    )
    user_message = _prompt.to_messages(
            system_prompt_input=system_prompt,
            user_input=context_str,
    )
    messages = conversation_history + user_message
    client = get_target_client()
    return client.complete(messages=messages)