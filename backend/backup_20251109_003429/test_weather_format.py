#!/usr/bin/env python3
"""
Quick test script to demonstrate the weather API response format
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fetch_weather_data import WeatherFetcher
from fetch_aqi_data import AQIFetcher
import json
from datetime import datetime

def parse_weather_data(weather_data):
    """Parse weather data to extract key information"""
    if not weather_data:
        return None
    
    parsed = {
        "location_name": weather_data.get("locationName"),
        "forecast_periods": []
    }
    
    weather_elements = weather_data.get("weatherElement", [])
    
    # Get all time periods from the first element
    if weather_elements:
        time_periods = weather_elements[0].get("time", [])
        
        for time_index, time_period in enumerate(time_periods):
            period_data = {
                "start_time": time_period.get("startTime"),
                "end_time": time_period.get("endTime")
            }
            
            # Extract data for each element at this time period
            for element in weather_elements:
                element_name = element.get("elementName")
                times = element.get("time", [])
                
                if time_index < len(times):
                    parameter = times[time_index].get("parameter", {})
                    param_name = parameter.get("parameterName")
                    
                    if element_name == "Wx":
                        period_data["weather_condition"] = param_name
                    elif element_name == "PoP":
                        period_data["rain_probability"] = f"{param_name}%"
                    elif element_name == "MinT":
                        period_data["min_temperature"] = f"{param_name}°C"
                    elif element_name == "MaxT":
                        period_data["max_temperature"] = f"{param_name}°C"
                    elif element_name == "CI":
                        period_data["comfort_index"] = param_name
            
            parsed["forecast_periods"].append(period_data)
    
    return parsed


def get_aqi_level_name(aqi_value):
    """Get AQI level name based on value"""
    try:
        aqi = int(aqi_value)
        if aqi <= 50:
            return "良好 (Good)"
        elif aqi <= 100:
            return "普通 (Moderate)"
        elif aqi <= 150:
            return "對敏感族群不健康 (Unhealthy for Sensitive Groups)"
        elif aqi <= 200:
            return "對所有族群不健康 (Unhealthy)"
        elif aqi <= 300:
            return "非常不健康 (Very Unhealthy)"
        else:
            return "危害 (Hazardous)"
    except (ValueError, TypeError):
        return "未知 (Unknown)"


def format_aqi_data(aqi_station):
    """Format AQI data with level names"""
    if not aqi_station:
        return None
    
    aqi_value = aqi_station.get('aqi', 'N/A')
    
    return {
        "site_name": aqi_station.get('sitename', 'N/A'),
        "county": aqi_station.get('county', 'N/A'),
        "aqi": aqi_value,
        "aqi_level": get_aqi_level_name(aqi_value),
        "status": aqi_station.get('status', 'N/A'),
        "pm25": aqi_station.get('pm2.5', 'N/A'),
        "pollutant": aqi_station.get('pollutant', 'N/A'),
        "publish_time": aqi_station.get('publishtime', 'N/A')
    }


def main():
    print("=" * 80)
    print("Testing Weather API Response Format")
    print("=" * 80)
    
    location = "臺北市"
    
    # Fetch weather
    print(f"\n📍 Fetching weather for {location}...")
    weather_fetcher = WeatherFetcher(locations=[location])
    
    if weather_fetcher.fetch_data(verify_ssl=False):
        weather_raw = weather_fetcher.get_location_weather(location)
        parsed_weather = parse_weather_data(weather_raw)
        
        if parsed_weather and parsed_weather.get("forecast_periods"):
            current_period = parsed_weather["forecast_periods"][0]
            
            print("\n✅ Weather Data (Current Period):")
            print(json.dumps({
                "location_name": parsed_weather["location_name"],
                "current_period": current_period
            }, ensure_ascii=False, indent=2))
    
    # Fetch AQI
    print(f"\n📍 Fetching AQI for {location}...")
    aqi_fetcher = AQIFetcher()
    
    if aqi_fetcher.fetch_data(verify_ssl=False):
        aqi_stations = aqi_fetcher.get_stations_by_county(location)
        
        if aqi_stations:
            formatted_aqi = format_aqi_data(aqi_stations[0])
            
            print("\n✅ AQI Data (with level names):")
            print(json.dumps(formatted_aqi, ensure_ascii=False, indent=2))
    
    # Show complete response format
    print("\n" + "=" * 80)
    print("Expected API Response Format:")
    print("=" * 80)
    
    expected_response = {
        "location": "臺北市",
        "timestamp": datetime.now().isoformat(),
        "weather": {
            "location_name": "臺北市",
            "temperature": "24.5°C",               # Current temp (avg of min/max)
            "weather_condition": "晴時多雲",        # Wx
            "rain_probability_3h": "12.5%",        # PoP averaged over next 3 hours
            "comfort_index": "舒適",                # CI
            "forecast_period": {
                "start_time": "2025-11-08 18:00:00",
                "end_time": "2025-11-09 06:00:00"
            }
        },
        "aqi": {
            "site_name": "士林",
            "county": "臺北市",
            "aqi": "54",
            "aqi_level": "普通 (Moderate)",
            "status": "普通",
            "pm25": "13",
            "pollutant": "懸浮微粒",
            "publish_time": "2025/11/08 19:00:00"
        }
    }
    
    print(json.dumps(expected_response, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 80)
    print("✅ API Response Summary:")
    print("   • temperature: Current temperature (average of min/max from current period)")
    print("   • weather_condition (Wx): Weather description (e.g., 晴時多雲)")
    print("   • rain_probability_3h (PoP): AVERAGED over next 3 hours")
    print("   • aqi: AQI value with level names (Chinese + English)")
    print("=" * 80)


if __name__ == "__main__":
    main()
