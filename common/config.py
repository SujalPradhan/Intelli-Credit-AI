import os

class Settings:
    APP_NAME: str = "Intelli-Credit AI Decisioning System"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
