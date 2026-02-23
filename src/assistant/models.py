from dataclasses import dataclass
from typing import List, Literal

Difficulty = Literal["easy", "medium", "hard"]

@dataclass
class ExplainRequest:
    topic: str
    audience: str = "beginner"
    format: str = "concise"

@dataclass
class QuizRequest:
    topic: str
    n: int = 5
    difficulty: Difficulty = "medium"

@dataclass
class QuizChoice:
    label: str
    text: str

@dataclass
class QuizQuestion:
    question: str
    choices: List[QuizChoice]
    correct_label: str
    rationale: str

@dataclass
class ExplainResponse:
    topic: str
    explanation: str

@dataclass
class QuizResponse:
    topic: str
    difficulty: Difficulty
    questions: List[QuizQuestion]
