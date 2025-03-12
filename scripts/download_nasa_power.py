import os
import time
import requests
import config

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

# Function to download data for a given year


def download_data(year):
    start_date = f"{year}0101"
    end_date = f"{year}1231"

    url = (
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?"
        f"start={start_date}&end={end_date}&latitude={config.LATITUDE}&longitude={config.LONGITUDE}"
        f"&community=re&parameters={config.PARAMETERS}&format=csv"
        f"&user=fahim&header=true&time-standard=lst"
    )

    file_path = f"data/nasa_power_{year}.csv"

    for attempt in range(5):  # Max retries
        try:
            print(f"📡 Downloading data for {year}...")
            response = requests.get(url, timeout=60)

            if response.status_code == 200:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"✅ Successfully downloaded {year}.")
                return file_path
            else:
                print(f"⚠️ API Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Attempt {attempt+1} failed: {e}")
            time.sleep(5)

    print(f"❌ Failed to download {year} after multiple attempts.")
    return None


# Run downloader for all years
for year in range(config.START_YEAR, config.END_YEAR + 1):
    download_data(year)

print("🎉 Download completed!")
