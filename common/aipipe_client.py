from openai import OpenAI
from common.config import settings


def get_aipipe_client() -> OpenAI:
    """Initialize and return an OpenAI client configured for AIPipe."""
    # Since AIPipe is an OpenAI-compatible endpoint, we use the standard OpenAI client
    # and override the base_url.
    client = OpenAI(
        api_key=settings.AIPIPE_API_KEY or "sk-placeholder", 
        base_url="https://aipipe.org/openai/v1"
    )
    return client
