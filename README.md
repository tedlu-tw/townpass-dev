# TownPass Development Scripts

Python scripts for fetching data from various Taiwan public APIs.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your API keys:
     ```
     CWA_API_KEY=your_actual_api_key_here
     MOENV_API_KEY=your_actual_api_key_here
     ```

3. **Fix SSL Certificate Issues (macOS only, if needed):**
   
   If you encounter SSL certificate errors, run:
   ```bash
   ./fix_ssl_certificates.sh
   ```
   
   Or manually:
   ```bash
   /Applications/Python*/Install\ Certificates.command
   ```
   
   Alternatively, upgrade certifi:
   ```bash
   pip install --upgrade certifi
   ```

## Scripts

### 1. YouBike Data Fetcher (`fetch_youbike_data.py`)

Fetches real-time YouBike 2.0 station data from Taipei City.

**Usage:**
```bash
python fetch_youbike_data.py
```

**Features:**
- Fetches data from all YouBike 2.0 stations
- Filter stations by area/district
- Find stations with available bikes
- Display station details and system summary
- Save data to `data/youbike_data.json`

### 2. Weather Data Fetcher (`fetch_weather_data.py`)

Fetches 36-hour weather forecast from Taiwan Central Weather Administration (CWA).

**Usage:**
```bash
python fetch_weather_data.py
```

**Features:**
- Fetches weather data for Taipei, New Taipei, and Keelung
- Weather elements: condition, rain probability, comfort index, min/max temperature
- Rain alerts (configurable threshold)
- Detailed and summary views
- Save data to `data/weather_data.json`

**Get API Key:**
Register at https://opendata.cwa.gov.tw/ to get your free API key.

### 3. AQI Data Fetcher (`fetch_aqi_data.py`)

Fetches real-time Air Quality Index (AQI) data from Taiwan Ministry of Environment.

**Usage:**
```bash
python fetch_aqi_data.py
```

**Features:**
- Fetches AQI data from 86 monitoring stations nationwide
- Displays PM2.5, PM10, O3, CO, SO2, NO2 levels
- AQI status classification (良好/普通/不健康)
- County-specific summaries
- Unhealthy air quality alerts (configurable threshold)
- Weather conditions (wind speed/direction)
- Save data to `data/aqi_data.json`

**Get API Key:**
Register at https://data.moenv.gov.tw/ to get your free API key.

## Data Sources

- **YouBike 2.0**: https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json
- **Weather Forecast**: https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001
- **Air Quality Index (AQI)**: https://data.moenv.gov.tw/api/v2/aqx_p_432

## Output

All fetched data is saved to the `data/` directory:
- `data/youbike_data.json` - YouBike station data
- `data/weather_data.json` - Weather forecast data
- `data/aqi_data.json` - Air quality index data

## Mock Data

Sample data files for testing:
- `youbike_data_mock.json` - Sample YouBike station data
- `weather_data_mock.json` - Sample weather forecast data

## Project Structure

```
townpass-dev/
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── fetch_youbike_data.py       # YouBike data fetcher
├── fetch_weather_data.py       # Weather data fetcher
├── fetch_aqi_data.py           # AQI data fetcher
├── youbike_data_mock.json      # Sample YouBike data
├── weather_data_mock.json      # Sample weather data
└── data/                       # Output directory (git ignored)
    ├── youbike_data.json       # Fetched YouBike data
    ├── weather_data.json       # Fetched weather data
    └── aqi_data.json           # Fetched AQI data
```

## License

This project is for development purposes.
