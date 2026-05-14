import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = "project-7cd9107f-68c7-4127-848"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"

DATA_DIR = "data"
INPUT_FILE = os.path.join(DATA_DIR, "lockers_warszawa_500.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "lockers_warszawa_scored.json")