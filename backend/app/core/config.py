import os
from functools import lru_cache
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    spotify_client_id: str | None = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret: str | None = os.getenv("SPOTIFY_CLIENT_SECRET")
    spotify_redirect_uri: str = os.getenv(
        "SPOTIFY_REDIRECT_URI",
        "http://127.0.0.1:8000/api/music/callback"
    )
    frontend_origin: str = os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5500"
    )


@lru_cache
def get_settings():
    return Settings()