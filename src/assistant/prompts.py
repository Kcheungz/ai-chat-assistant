EXPLAIN_SYSTEM = """You are a helpful study tutor.
Be accurate, structured, and concise. Avoid fluff.
If the user asks about a technical topic, include small practical examples."""

def explain_user(topic: str, audience: str, fmt: str) -> str:
    return f"""Explain the topic: "{topic}"

Audience: {audience}
Format: {fmt}

Requirements:
- Use clear headings
- Include a short example
- End with 3 quick check questions (no answers)"""


QUIZ_SYSTEM = """You are an exam writer.
Produce challenging questions that test understanding, not trivia.
Always return valid JSON only. No extra text."""

def quiz_user(topic: str, n: int, difficulty: str) -> str:
    return f"""Create a quiz on: "{topic}"

Number of questions: {n}
Difficulty: {difficulty}

Return JSON with this shape:
{{
  "topic": "...",
  "difficulty": "easy|medium|hard",
  "questions": [
    {{
      "question": "...",
      "choices": [
        {{"label": "A", "text": "..."}},
        {{"label": "B", "text": "..."}},
        {{"label": "C", "text": "..."}},
        {{"label": "D", "text": "..."}}
      ],
      "correct_label": "A|B|C|D",
      "rationale": "..."
    }}
  ]
}}

Rules:
- Exactly 4 choices per question
- One correct label
- Rationales must explain why the correct option is correct
"""
