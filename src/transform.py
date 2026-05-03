import json
from pathlib import Path
import pandas as pd
from config import RAW_DIR, PROCESSED_DIR, SERIES

def load_raw_json(series_id: str) -> dict:
    file_path = RAW_DIR / f"{series_id}.json"

    if not file_path.exists():
        raise FileNotFoundError(f"Raw file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def transform_observations(series_id: str, data: dict) -> pd.DataFrame:
    observations = data.get("observations", [])

    if not observations:
        return pd.DataFrame(columns=["series_id", "series_name", "date", "value"])

    df = pd.DataFrame(observations)

    df = df[["date", "value"]].copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df["series_id"] = series_id
    df["series_name"] = SERIES.get(series_id, series_id)

    df = df.dropna(subset=["date", "value"])
    df = df.sort_values("date").reset_index(drop=True)

    return df[["series_id", "series_name", "date", "value"]]

def save_processed_csv(series_id: str, df: pd.DataFrame) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    file_path = PROCESSED_DIR / f"{series_id}_clean.csv"

    df.to_csv(file_path, index=False)

    return file_path
def main():
    for series_id in SERIES:
        print(f"Transforming {series_id}...")
        raw_data = load_raw_json(series_id)
        clean_df = transform_observations(series_id, raw_data)
        saved_path = save_processed_csv(series_id, clean_df)
        print(f"Saved cleaned CSV to: {saved_path} ({len(clean_df)} rows)")

if __name__ == "__main__":
    main()