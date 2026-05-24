import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Email/SMTP Configuration
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
try:
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
except ValueError:
    SMTP_PORT = 587

# Local Music Configuration
MUSIC_DIR = os.getenv("MUSIC_DIR", "")

# Voice Engine Settings
VOICE_RATE = 180      # Speed (words per minute)
VOICE_VOLUME = 1.0    # Volume (0.0 to 1.0)
VOICE_GENDER_INDEX = 1  # Index of the voice (usually 0 for male, 1 for female)

# Default Web URLs
WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "stack overflow": "https://www.stackoverflow.com",
    "gmail": "https://mail.google.com",
}
