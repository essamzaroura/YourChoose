# config.py - Stores API keys and configurations

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get API key from environment (or define it here)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "yoAIzaSyAl67Y10Vb41YPrR0SwvLy9DHSTO8AjoHE")

# Other configuration settings (add as needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
