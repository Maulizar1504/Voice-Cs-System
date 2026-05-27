import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMP_DIR = os.path.join(BASE_DIR, "output", "temp")
OUTPUT_AUDIO_DIR = os.path.join(BASE_DIR, "output", "audio")
LOG_DIR = os.path.join(BASE_DIR, "log")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")