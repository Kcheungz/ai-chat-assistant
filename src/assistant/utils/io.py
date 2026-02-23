import json
from pathlib import Path
from typing import Any


def read_text_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: str, data: Any) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))
