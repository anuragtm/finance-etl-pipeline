import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from config import BASE_URL, SERIES, RAW_DIR

load_dotenv()


def fetch_series(series_id: str) -> dict:
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise ValueError("FRED_API_KEY not found in .env file")

    params = {"series_id": series_id,
        "api_key": api_key,
        "file_type": "json",}

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw_json(series_id: str, data: dict) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    file_path = RAW_DIR / f"{series_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return file_path


def main():
    for series_id in SERIES:
        print(f"Fetching {series_id}...")
        data = fetch_series(series_id)
        saved_path = save_raw_json(series_id, data)
        print(f"Saved raw JSON to: {saved_path}")


if __name__ == "__main__":
    main()