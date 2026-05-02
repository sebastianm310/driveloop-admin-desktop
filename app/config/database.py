import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return os.getenv("API_URL")