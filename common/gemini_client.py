from google import genai
from common.config import settings


def get_gemini_client():
    """Initialize and return a google.genai Client instance."""
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return client
