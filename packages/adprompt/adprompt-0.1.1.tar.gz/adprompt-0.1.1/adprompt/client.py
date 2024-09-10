from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletion

from adprompt.chat import ChatResponse
from adprompt.role import BaseRole


class AdpromptClient:

    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model

    def _chat(self, messages: List[dict], temperature: float = 0.3, **kwargs) -> ChatCompletion:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            **kwargs,
        )
        return completion

    def chat(self, role: BaseRole, content: str, **kwargs) -> ChatResponse:
        messages = role.get_role_context()
        messages.append({
            'role': 'user',
            'content': content,
        })
        completion = self._chat(messages, **kwargs)
        result = role.post_process(completion)
        return result
