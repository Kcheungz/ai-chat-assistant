from dataclasses import dataclass
import os
from pathlib import Path
import sys
from dotenv import load_dotenv

def _default_env_path() -> Path | None:
    """
    Prefer .env next to the executable when frozen (PyInstaller),
    otherwise use project root (.env in current working dir).
    """
    try:
        if getattr(sys, "frozen", False):
            exe_dir = Path(sys.executable).resolve().parent
            candidate = exe_dir / ".env"
            return candidate if candidate.exists() else None
    except Exception:
        return None
    return None

# Try loading .env next to exe first, then fallback to normal search
env_path = _default_env_path()
if env_path:
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str

def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    return Settings(api_key=api_key, model=model)
