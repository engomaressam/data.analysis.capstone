# Build Clean Cyclistic Dataset (Ingestion + Cleaning)
# Author: Continuation by Trae AI Assistant
# Date: Current Date
# Purpose: Ingest recent Divvy/Cyclistic monthly CSVs and build a cleaned, processed dataset

import os
import re
import shutil
from datetime import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd

# -------------------------------
# Configuration
# -------------------------------
PROJECT_ROOT = os.getcwd()
DOWNLOADED_DIR = os.path.join("data", "downloaded")
RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "cyclistic_cleaned.csv")

# How many most-recent months to include
MONTHS_TO_INCLUDE = 12

# Pattern for monthly folders (e.g., 202412-divvy-tripdata)
MONTHLY_FOLDER_REGEX = re.compile(r"^(\d{6})-divvy-tripdata$")

# -------------------------------
# Helpers
# -------------------------------

def list_monthly_downloaded() -> List[Tuple[str, str]]:
    """Return list of (yyyymm, folder_path) for monthly downloaded tripdata folders."""
    items = []
    base = DOWNLOADED_DIR
    if not os.path.isdir(base):
        print(f"❌ Downloaded directory not found: {base}")
        return items

    for name in os.listdir(base):
        full = os.path.join(base, name)
        if os.path.isdir(full):
            m = MONTHLY_FOLDER_REGEX.match(name)
            if m:
                yyyymm = m.group(1)
                items.append((yyyymm, full))
    # Sort by yyyymm ascending
    items.sort(key=lambda x: x[0])
    return items


def copy_to_raw(monthly_items: List[Tuple[str, str]]) -> List[str]:
    """Copy selected monthly CSVs to data/raw/<folder>/, return list of raw file paths."""
    os.makedirs(RAW_DIR, exist_ok=True)
    raw_files = []
    for yyyymm, src_folder in monthly_items:
        # Expect filename like 202412-divvy-tripdata.csv inside folder
        expected_csv = os.path.join(src_folder, f"{yyyymm}-divvy-tripdata.csv")
        if not os.path.isfile(expected_csv):
            # If not found, try glob for CSV in folder
            candidates = [f for f in os.listdir(src_folder) if f.lower().endswith('.csv')]
            if candidates:
                expected_csv = os.path.join(src_folder, candidates[0])
            else:
                print(f"⚠️ No CSV found in {src_folder}; skipping")
                continue
        # Create raw subfolder and copy
        raw_subdir = os.path.join(RAW_DIR, f"{yyyymm}-divvy-tripdata")
        os.makedirs(raw_subdir, exist_ok=True)
        dst_csv = os.path.join(raw_subdir, os.path.basename(expected_csv))
        try:
            shutil.copy2(expected_csv, dst_csv)
            raw_files.append(dst_csv)
        except Exception as e:
            print(f"❌ Failed to copy {expected_csv} -> {dst_csv}: {e}")
    return raw_files


def select_recent_months(all_months: List[Tuple[str, str]], n: int) -> List[Tuple[str, str]]:
    """Select last n months from the list of (yyyymm, folder_path)."""
    if not all_months:
        return []
    return all_months[-n:]


# -------------------------------
# Cleaning Utilities
# -------------------------------

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure standard columns and types for Divvy monthly data since 2020."""
    # Expected columns (post-2020 schema)
    expected_cols = {
        'ride_id', 'rideable_type', 'started_at', 'ended_at',
        'start_station_name', 'start_station_id',
        'end_station_name', 'end_station_id',
        'start_lat', 'start_lng', 'end_lat', 'end_lng',
        'member_casual'
    }
    # Normalize column names to lower
    df.columns = [c.strip() for c in df.columns]
    # If case differences exist, align using lowercase map
    lower_map = {c.lower(): c for c in df.columns}
    # Rename to lowercase first
    df.rename(columns={c: c.lower() for c in df.columns}, inplace=True)

    # Drop unexpected columns but keep known ones
    cols_to_keep = [c for c in df.columns if c in expected_cols]
    df = df[cols_to_keep].copy()

    # Fill missing expected columns with NaN
    for c in expected_cols:
        if c not in df.columns:
            df[c] = np.nan

    return df[list(expected_cols)]


def derive_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features and clean fields."""
    # Parse datetime
    df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
    df['ended_at'] = pd.to_datetime(df['ended_at'], errors='coerce')

    # Remove rows with invalid datetimes
    df = df.dropna(subset=['started_at', 'ended_at'])

    # Duration in minutes
    df['ride_duration_minutes'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60.0

    # Filter unrealistic durations
    df = df[(df['ride_duration_minutes'] > 1) & (df['ride_duration_minutes'] < 1440)]

    # Ensure end after start
    df = df[df['ended_at'] > df['started_at']]

    # Text normalization
    for col in ['rideable_type', 'member_casual', 'start_station_name', 'end_station_name']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            if col in ['rideable_type', 'member_casual']:
                df[col] = df[col].str.lower()

    # Handle station nulls
    df['start_station_name'] = df['start_station_name'].fillna('Unknown')
    df['end_station_name'] = df['end_station_name'].fillna('Unknown')
    df['start_station_id'] = df['start_station_id'].fillna('Unknown')
    df['end_station_id'] = df['end_station_id'].fillna('Unknown')

    # Validate member type
    df = df[df['member_casual'].isin(['member', 'casual'])]

    # Derived temporal variables
    df['date'] = df['started_at'].dt.date
    # Make Sunday=0, Monday=1, ... Saturday=6
    df['day_of_week'] = ((df['started_at'].dt.dayofweek + 1) % 7).astype(int)
    df['hour_of_day'] = df['started_at'].dt.hour.astype(int)
    df['month'] = df['started_at'].dt.month.astype(int)
    df['day_type'] = np.where(df['day_of_week'].isin([0, 6]), 'Weekend', 'Weekday')

    def time_bucket(h: int) -> str:
        if 5 <= h <= 11:
            return 'Morning'
        if 12 <= h <= 16:
            return 'Afternoon'
        if 17 <= h <= 21:
            return 'Evening'
        return 'Night'

    df['time_of_day'] = df['hour_of_day'].apply(time_bucket)

    return df


# -------------------------------
# Main Pipeline
# -------------------------------

def build_clean_dataset():
    print("\n=== Cyclistic Dataset Build: Ingestion + Cleaning ===")
    print(f"Project root: {PROJECT_ROOT}")

    all_months = list_monthly_downloaded()
    if not all_months:
        print("❌ No monthly downloaded folders found.")
        return

    selected = select_recent_months(all_months, MONTHS_TO_INCLUDE)
    print(f"📦 Found {len(all_months)} monthly folders; selecting last {len(selected)} months:")
    print("   " + ", ".join([m for m, _ in selected]))

    # Copy into raw for reproducibility
    raw_files = copy_to_raw(selected)
    print(f"📁 Copied {len(raw_files)} CSV files into {RAW_DIR}")

    if not raw_files:
        print("❌ No raw files available after copy; aborting")
        return

    # Read, standardize, concat
    dfs = []
    for path in raw_files:
        try:
            df = pd.read_csv(path)
            df = standardize_columns(df)
            dfs.append(df)
        except Exception as e:
            print(f"⚠️ Skipping file due to read error: {path} -> {e}")

    if not dfs:
        print("❌ No dataframes loaded; aborting")
        return

    combined = pd.concat(dfs, axis=0, ignore_index=True)
    print(f"🧮 Combined records before dedup: {len(combined):,}")

    # Deduplicate by ride_id
    if 'ride_id' in combined.columns:
        combined = combined.drop_duplicates(subset=['ride_id'])
    print(f"🧹 Records after dedup: {len(combined):,}")

    # Derive features and filter
    cleaned = derive_features(combined)
    print(f"✅ Records after cleaning/filters: {len(cleaned):,}")

    # Output
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)

    # Summary
    summary = {
        'total_records_cleaned': len(cleaned),
        'period_start': str(pd.to_datetime(cleaned['date']).min()) if len(cleaned) else None,
        'period_end': str(pd.to_datetime(cleaned['date']).max()) if len(cleaned) else None,
        'avg_duration_minutes': round(float(cleaned['ride_duration_minutes'].mean()), 2) if len(cleaned) else None,
        'members_pct': round(100 * (cleaned['member_casual'] == 'member').mean(), 2) if len(cleaned) else None,
        'casual_pct': round(100 * (cleaned['member_casual'] == 'casual').mean(), 2) if len(cleaned) else None,
    }
    print("\n📊 Build Summary:")
    for k, v in summary.items():
        print(f" - {k}: {v}")

    print(f"\n💾 Saved cleaned dataset -> {OUTPUT_FILE}")
    print("🚀 Ready for EDA: analysis/exploratory/cyclistic_eda.py expects this file path")


if __name__ == "__main__":
    build_clean_dataset()