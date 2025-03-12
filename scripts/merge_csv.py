import os
import pandas as pd
import config

# Get all downloaded files
csv_files = [
    f"data/{file}" for file in os.listdir("data") if file.endswith(".csv")]

# Merge all CSV files
if csv_files:
    print("🔄 Merging all files...")
    dataframes = [pd.read_csv(file, skiprows=9)
                  for file in csv_files]  # Skip header rows
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Save merged file
    merged_df.to_csv(config.OUTPUT_FILE, index=False)
    print(f"✅ Merged dataset saved as '{config.OUTPUT_FILE}'")
else:
    print("❌ No files found for merging.")
