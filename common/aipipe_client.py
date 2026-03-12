from openai import AsyncOpenAI
from common.config import settings


def get_aipipe_client() -> AsyncOpenAI:
    """Initialize and return an async OpenAI client configured for AIPipe."""
    client = AsyncOpenAI(
        api_key=settings.AIPIPE_API_KEY or "sk-placeholder", 
        base_url="https://aipipe.org/openai/v1"
    )
    return client
