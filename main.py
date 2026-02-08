"""
NOAA Weather Data Cleaning Script
--------------------------------
- Loads raw NOAA weather data
- Cleans and converts columns to correct types
- Handles missing and invalid values
- Saves a cleaned dataset for analysis and forecasting
"""

import pandas as pd
import numpy as np

RAW_DATA_PATH = "jfk_weather.csv"
CLEAN_DATA_PATH = "jfk_weather_cleaned.csv"

print("Loading local dataset...")

# Load data
df = pd.read_csv(
    RAW_DATA_PATH,
    parse_dates=["DATE"],
    low_memory=False
)

# Standardize column names
df.columns = df.columns.str.strip().str.upper()

# Replace known missing markers
df.replace(["M", "NA", "N/A", "", " "], np.nan, inplace=True)

# Convert numeric columns
numeric_columns = [
    "HOURLYDRYBULBTEMPF",
    "HOURLYRELATIVEHUMIDITY",
    "HOURLYWINDVELOCITY",
    "HOURLYVISIBILITY",
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop rows missing critical data
df.dropna(subset=["DATE", "HOURLYDRYBULBTEMPF"], inplace=True)

# Sort for time-series correctness
df.sort_values("DATE", inplace=True)
df.reset_index(drop=True, inplace=True)

# Save cleaned dataset
df.to_csv(CLEAN_DATA_PATH, index=False)
print("Cleaned data saved successfully.")
