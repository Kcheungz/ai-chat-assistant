import json
from typing import Any, Dict

from openai import OpenAI
from assistant.utils.errors import APIError, ParseError


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat_text(self, system: str, user: str) -> str:
        """
        Send a standard chat completion request and return raw text.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            raise APIError(f"OpenAI request failed: {e}") from e

    def chat_json(self, system: str, user: str) -> Dict[str, Any]:
        """
        Ask the model to return JSON only and parse it safely.
        """
        text = self.chat_text(system, user).strip()

        try:
            return json.loads(text)
        except Exception as e:
            raise ParseError(
                f"Model did not return valid JSON.\nRaw output:\n{text}"
            ) from e
