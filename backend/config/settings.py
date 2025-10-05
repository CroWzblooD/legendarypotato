"""
Load environment variables from .env file.
Use os.getenv() directly throughout the application.
"""
from dotenv import load_dotenv

# Load .env file once on import
load_dotenv()
