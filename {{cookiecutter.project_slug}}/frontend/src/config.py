import os
from pathlib import Path

API_BASE_URL = os.environ.get("API_BASE_URL", "http://api:8000")
DATABASE_URL = os.environ.get("DATABASE_URL", None)

BASE_DIR = Path("/app")