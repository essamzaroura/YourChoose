# config.py - Stores API keys and configurations

import os
from dotenv import load_dotenv
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load environment variables from a .env file
load_dotenv()

# Get API key from environment (secure way)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAl67Y10Vb41YPrR0SwvLy9DHSTO8AjoHE")

# Other configuration settings (add as needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")