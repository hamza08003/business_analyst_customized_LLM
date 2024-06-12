import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
APIFY_API_KEY = os.getenv("APIFY_API_TOKEN")
