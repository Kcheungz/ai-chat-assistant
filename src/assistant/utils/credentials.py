import keyring

SERVICE_NAME = "StudyAssistantOpenAI"
ACCOUNT_NAME = "OPENAI_API_KEY"

def get_api_key() -> str | None:
    return keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)

def set_api_key(api_key: str) -> None:
    keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, api_key.strip())

def clear_api_key() -> None:
    keyring.delete_password(SERVICE_NAME, ACCOUNT_NAME)
