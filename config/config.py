"""
Configuration module for CP Automated LMS & Portfolio
Handles file paths, environment variables, and credential resolution.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
WEB_DIR = BASE_DIR / "web"
WEB_DATA_DIR = WEB_DIR / "data"

# Ensure output directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load .env if present
load_dotenv(BASE_DIR / ".env")

# Local source Excel workbooks (existing CP notes & sheets)
LOCAL_EXCEL_FILES = [
    BASE_DIR / "Bản sao của code cùng Coản Coản.xlsx",
    BASE_DIR / "Link Em Phung Duc Nong 15p.xlsx",
]

# Output files
MASTER_EXCEL_PATH = BASE_DIR / "master_cp_data.xlsx"
FRONTEND_DATA_JSON = WEB_DATA_DIR / "data.json"

# Google Sheets Config
GOOGLE_SPREADSHEET_ID = os.getenv("GOOGLE_SPREADSHEET_ID", "")
GOOGLE_SPREADSHEET_TITLE = os.getenv("GOOGLE_SPREADSHEET_TITLE", "Master CP Learning System")
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "")

# Firebase Config
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_SERVICE_ACCOUNT_KEY = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "")

# Firestore Collections
COLLECTIONS = {
    "EXERCISES": "exercises",
    "MATERIALS": "materials",
    "PROJECTS": "projects",
    "ROADMAP": "roadmap",
    "STATS": "stats",
}

def get_service_account_dict():
    """
    Resolves Firebase/Google service account credentials.
    Priority:
    1. FIREBASE_SERVICE_ACCOUNT_KEY env var (raw JSON string or file path)
    2. GOOGLE_SHEETS_CREDENTIALS env var (raw JSON string or file path)
    3. GOOGLE_APPLICATION_CREDENTIALS env var (file path)
    4. Local file: config/service_account.json
    Returns dict if found, else None.
    """
    for candidate in [
        FIREBASE_SERVICE_ACCOUNT_KEY,
        GOOGLE_SHEETS_CREDENTIALS,
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""),
    ]:
        if not candidate:
            continue
        # Case A: candidate is a path to an existing file
        if os.path.exists(candidate):
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Config] Warning: Failed to parse credentials from file '{candidate}': {e}")
        # Case B: candidate is raw JSON string
        try:
            trimmed = candidate.strip()
            if trimmed.startswith("{") and trimmed.endswith("}"):
                return json.loads(trimmed)
        except Exception:
            pass

    # Check default local path
    default_json = CONFIG_DIR / "service_account.json"
    if default_json.exists():
        try:
            with open(default_json, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Config] Warning: Failed to parse {default_json}: {e}")

    return None
