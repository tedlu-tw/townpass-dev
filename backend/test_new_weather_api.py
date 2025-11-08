#!/usr/bin/env python3
"""
Test script for new weather API
Tests the updated F-D0047-061 API integration
"""

from scripts.fetch_weather_data import WeatherFetcher
from routes.weather_routes import parse_weather_data, get_current_temperature, calculate_average_pop_next_3_hours

def test_fetch_and_parse():
    """Test fetching and parsing weather data"""
    print("="*80)
    print("Testing New Weather API (F-D0047-061)")
    print("="*80)
    
    # Initialize fetcher
    fetcher = WeatherFetcher()
    
    # Fetch data
    print("\n1. Fetching data from CWA API...")
    if not fetcher.fetch_data(verify_ssl=False):
        print("❌ Failed to fetch data")
        return False
    
    print("✅ Data fetched successfully")
    
    # Test finding nearest location by coordinates
    print("\n2. Finding nearest location to coordinates (25.0374865, 121.5647688)...")
    nearest = fetcher.find_nearest_location(25.0374865, 121.5647688)
    
    if not nearest:
        print("❌ Failed to find nearest location")
        return False
    
    location_name = nearest.get("LocationName")
    lat = nearest.get("Latitude")
    lng = nearest.get("Longitude")
    print(f"✅ Found: {location_name} (lat: {lat}, lng: {lng})")
    
    # Parse weather data
    print("\n3. Parsing weather data...")
    parsed = parse_weather_data(nearest)
    
    if not parsed:
        print("❌ Failed to parse weather data")
        return False
    
    print(f"✅ Parsed data for: {parsed.get('location_name')}")
    print(f"   Forecast periods: {len(parsed.get('forecast_periods', []))}")
    print(f"   Temperature records: {len(parsed.get('temperature_data', []))}")
    
    # Get current temperature
    print("\n4. Getting current temperature...")
    current_temp = get_current_temperature(parsed.get("temperature_data", []))
    if current_temp:
        print(f"✅ Current temperature: {current_temp}°C")
    else:
        print("⚠️  No temperature data available")
    
    # Get rain probability
    print("\n5. Getting rain probability...")
    rain_prob = calculate_average_pop_next_3_hours(parsed.get("forecast_periods", []))
    print(f"✅ Current 3-hour rain probability: {rain_prob}%")
    
    # Show first forecast period
    if parsed.get("forecast_periods"):
        first_period = parsed["forecast_periods"][0]
        print("\n6. Current forecast period:")
        print(f"   Time: {first_period.get('start_time')} to {first_period.get('end_time')}")
        print(f"   Rain probability: {first_period.get('rain_probability')}%")
        desc = first_period.get('weather_description', '')
        if desc:
            print(f"   Description: {desc[:80]}...")
    
    print("\n" + "="*80)
    print("✅ All tests passed!")
    print("="*80)
    
    return True

if __name__ == "__main__":
    test_fetch_and_parse()
