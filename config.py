import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

SAMPLE_DATA_DIR = Path("data/sample_data")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")