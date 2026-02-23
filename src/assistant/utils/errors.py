class AssistantError(Exception):
    """Base exception for assistant-related errors."""


class ConfigError(AssistantError):
    """Configuration issues (missing API key, etc)."""


class APIError(AssistantError):
    """API call failures or network issues."""


class ParseError(AssistantError):
    """Model response parsing issues."""
