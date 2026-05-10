"""
Configuration module for AI Chat + Sync + Learning.
"""

import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# AI Configuration
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
GOOGLE_GEMINI_API_BASE = os.getenv("GOOGLE_GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta")
PUTER_AUTH_TOKEN = os.getenv("PUTER_AUTH_TOKEN")
PUTER_MODEL = os.getenv("PUTER_MODEL", "gpt-4o-mini")

# Determine AI provider based on available keys
if GOOGLE_GEMINI_API_KEY and not PUTER_AUTH_TOKEN:
    AI_PROVIDER = "gemini"
elif PUTER_AUTH_TOKEN and not GOOGLE_GEMINI_API_KEY:
    AI_PROVIDER = "puter"
else:
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower()  # Default to gemini

DEFAULT_MODEL = "gemini-1.5-flash"
MAX_TOKENS = 2048
TEMPERATURE = 0.7
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2

# App Settings
APP_NAME = "Humanoid AI Assistant"
APP_VERSION = "1.0.0"
WELCOME_MESSAGE = f"Welcome to {APP_NAME} v{APP_VERSION}!"
EXIT_COMMANDS = ["exit", "quit", "bye", "q"]

# Voice
VOSK_MODEL_LANG = "hi"
VOSK_MODEL_PATH = None

AVAILABLE_LANGUAGES = {
    "hi": {"name": "Hindi", "model_suffix": "hi"},
    "en-in": {"name": "English (Indian)", "model_suffix": "en-in"},
}

def get_available_language_codes():
    return list(AVAILABLE_LANGUAGES.keys())

def get_language_display_name(lang_code):
    return AVAILABLE_LANGUAGES.get(lang_code, {}).get("name", lang_code)

def get_model_suffix(lang_code):
    return AVAILABLE_LANGUAGES.get(lang_code, {}).get("model_suffix", lang_code)

# Database
DATABASE_PATH = "chat_memory.db"
USER_ACTIVITY_DB = "user_activity.db"
DATABASE_MAX_HISTORY_LOAD = 100
DATABASE_AUTO_LOAD = True

# Multi-Device Sync 
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/humanoid_sync")
DEVICE_ID = os.getenv("DEVICE_ID", None)
if DEVICE_ID is None:
    DEVICE_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"humanoid-assistant-{os.getenv('COMPUTERNAME', 'unknown')}"))

SYNC_CHANNELS = {
    "global_updates": "sync:global",
    "memory": "sync:memory",
    "tasks": "sync:tasks", 
    "context": "sync:context",
    "settings": "sync:settings"
}

# Auto-Learning Engine (NEW)
LEARNING_ENABLED = os.getenv("LEARNING_ENABLED", "true").lower() == "true"
LEARNING_DB_PATH = "learning_experiences.db"
LEARNING_ANALYSIS_DAYS = int(os.getenv("LEARNING_ANALYSIS_DAYS", "30"))
LEARNING_MIN_SAMPLES = 5
LEARNING_SUCCESS_THRESHOLD = 0.8

# Advanced Personality System (NEW)
PERSONALITY_ENABLED = os.getenv("PERSONALITY_ENABLED", "true").lower() == "true"
PERSONALITY_BASE_EMOTION = os.getenv("PERSONALITY_BASE_EMOTION", "neutral")
EMOTION_INTENSITY_SCALE = float(os.getenv("EMOTION_INTENSITY_SCALE", "1.0"))
PERSONALITY_TRAITS = {
    'friendly': float(os.getenv("PERSONALITY_FRIENDLY", "0.7")),
    'serious': float(os.getenv("PERSONALITY_SERIOUS", "0.3")),
    'playful': float(os.getenv("PERSONALITY_PLAYFUL", "0.5"))
}

# Note: API key validation in main.py

