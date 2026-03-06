import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
AIPIPE_API_KEY = os.getenv("AIPIPE_API_KEY")

class Settings:
    APP_NAME: str = "Intelli-Credit AI Decisioning System"
    GEMINI_API_KEY: str = GEMINI_API_KEY
    SERPER_API_KEY: str = SERPER_API_KEY
    AIPIPE_API_KEY: str = AIPIPE_API_KEY


settings = Settings()
