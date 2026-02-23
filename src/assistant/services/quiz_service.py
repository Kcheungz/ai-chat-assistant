from typing import List

from assistant.models import QuizRequest, QuizResponse, QuizQuestion, QuizChoice
from assistant.prompts import QUIZ_SYSTEM, quiz_user
from assistant.openai_client import OpenAIClient
from assistant.utils.errors import ParseError

class QuizService:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def quiz(self, req: QuizRequest) -> QuizResponse:
        data = self.client.chat_json(
            system=QUIZ_SYSTEM,
            user=quiz_user(req.topic, req.n, req.difficulty),
        )

        if "questions" not in data or not isinstance(data["questions"], list):
            raise ParseError("JSON missing 'questions' list")

        questions: List[QuizQuestion] = []
        for q in data["questions"]:
            choices = [QuizChoice(label=c["label"], text=c["text"]) for c in q["choices"]]
            questions.append(
                QuizQuestion(
                    question=q["question"],
                    choices=choices,
                    correct_label=q["correct_label"],
                    rationale=q["rationale"],
                )
            )

        return QuizResponse(
            topic=data.get("topic", req.topic),
            difficulty=data.get("difficulty", req.difficulty),
            questions=questions,
        )
