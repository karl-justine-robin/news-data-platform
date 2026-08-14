import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# =====================================================
# Configuration Validation
# =====================================================

def validate_config():
    required = {
        "DB_HOST": DB_HOST,
        "DB_NAME": DB_NAME,
        "DB_USER": DB_USER,
        "DB_PASSWORD": DB_PASSWORD,
    }

    missing = [
        name
        for name, value in required.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
        )


# =====================================================
# Project
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent

PIPELINE_NAME = os.getenv(
    "PIPELINE_NAME",
    "News Data Pipeline",
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)


# =====================================================
# Data
# =====================================================

DATA_DIR = PROJECT_ROOT / "data"

SAMPLE_DATA_DIR = DATA_DIR / "sample_data"


# =====================================================
# Database
# =====================================================

DB_HOST = os.getenv("DB_HOST")

DB_PORT = int(
    os.getenv("DB_PORT", 5432)
)

DB_NAME = os.getenv("DB_NAME")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")


# =====================================================
# API
# =====================================================

API_HOST = os.getenv(
    "API_HOST",
    "0.0.0.0",
)

API_PORT = int(
    os.getenv("API_PORT", 8000)
)

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)


# =====================================================
# Dashboard
# =====================================================

DASHBOARD_PORT = int(
    os.getenv("DASHBOARD_PORT", 8501)
)


def get_bool_env(
    name: str,
    default: bool = True,
) -> bool:

    value = os.getenv(name)

    if value is None:
        return default

    value = value.strip().lower()

    if value == "true":
        return True

    if value == "false":
        return False

    raise ValueError(
        f"Invalid boolean value for {name}: {value!r}. "
        "Expected 'true' or 'false'."
    )

# =====================================================
# Pipeline Controls
# =====================================================

ENABLE_INCREMENTAL = get_bool_env(
    "ENABLE_INCREMENTAL"
)

ENABLE_BRONZE = get_bool_env(
    "ENABLE_BRONZE"
)

ENABLE_SILVER = get_bool_env(
    "ENABLE_SILVER"
)

ENABLE_GOLD = get_bool_env(
    "ENABLE_GOLD"
)

ENABLE_WAREHOUSE = get_bool_env(
    "ENABLE_WAREHOUSE"
)