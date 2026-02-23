import argparse

from assistant.config import get_settings
from assistant.models import ExplainRequest, QuizRequest
from assistant.openai_client import OpenAIClient
from assistant.services.explain_service import ExplainService
from assistant.services.quiz_service import QuizService
from assistant.utils.errors import ConfigError, AssistantError
from assistant.utils.io import read_text_file, write_json, print_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="study-assistant",
        description="AI Study Assistant CLI (explanations + quiz questions)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # explain
    ex = sub.add_parser("explain", help="Generate an explanation for a topic")
    ex.add_argument("topic", type=str, help="Topic to explain")
    ex.add_argument("--audience", default="beginner", help="beginner | intermediate | advanced")
    ex.add_argument("--format", default="concise", help="concise | detailed")
    ex.add_argument("--save", help="Save JSON output to a file path")

    # quiz
    qz = sub.add_parser("quiz", help="Generate quiz questions for a topic")
    qz.add_argument("topic", nargs="?", help="Topic to quiz on (or use --from-file)")
    qz.add_argument("--from-file", dest="from_file", help="Read topic/context from a text file")
    qz.add_argument("--n", type=int, default=5, help="Number of questions")
    qz.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="medium")
    qz.add_argument("--save", help="Save JSON output to a file path")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = get_settings()

    if not settings.api_key:
        raise ConfigError("Missing OPENAI_API_KEY. Put it in a local .env file (not committed).")

    client = OpenAIClient(api_key=settings.api_key, model=settings.model)

    try:
        if args.cmd == "explain":
            service = ExplainService(client)
            resp = service.explain(ExplainRequest(
                topic=args.topic,
                audience=args.audience,
                format=args.format,
            ))

            out = {"topic": resp.topic, "explanation": resp.explanation}
            if args.save:
                write_json(args.save, out)
                print(f"Saved to {args.save}")
            else:
                print_json(out)

        elif args.cmd == "quiz":
            topic = args.topic

            if args.from_file:
                topic = read_text_file(args.from_file).strip()

            if not topic:
                raise AssistantError("Provide a topic or use --from-file")

            service = QuizService(client)
            resp = service.quiz(QuizRequest(topic=topic, n=args.n, difficulty=args.difficulty))

            out = {
                "topic": resp.topic,
                "difficulty": resp.difficulty,
                "questions": [
                    {
                        "question": q.question,
                        "choices": [{"label": c.label, "text": c.text} for c in q.choices],
                        "correct_label": q.correct_label,
                        "rationale": q.rationale,
                    }
                    for q in resp.questions
                ],
            }

            if args.save:
                write_json(args.save, out)
                print(f"Saved to {args.save}")
            else:
                print_json(out)

    except AssistantError as e:
        print(f"[error] {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
