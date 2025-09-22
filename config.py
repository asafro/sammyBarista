"""
Configuration file for SammyTheSpartanBarista.
Contains API keys and other configuration settings.
"""

# OpenRouter API Configuration
OPENROUTER_API_KEY = "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"

# Default model to use
DEFAULT_MODEL = "openai/gpt-3.5-turbo"

# MongoDB Configuration (optional - uses defaults if not set)
MONGODB_URL = "mongodb://localhost:27017/"
MONGODB_DATABASE = "coffee_db"
MONGODB_COLLECTION = "coffees"
