from assistant.models import ExplainRequest, ExplainResponse
from assistant.prompts import EXPLAIN_SYSTEM, explain_user
from assistant.openai_client import OpenAIClient

class ExplainService:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def explain(self, req: ExplainRequest) -> ExplainResponse:
        text = self.client.chat_text(
            system=EXPLAIN_SYSTEM,
            user=explain_user(req.topic, req.audience, req.format),
        )
        return ExplainResponse(topic=req.topic, explanation=text.strip())
