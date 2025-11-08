#!/usr/bin/env python3
"""
Test coordinate-based weather and AQI lookup
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_weather_with_coordinates():
    """Test weather endpoint with coordinates"""
    
    print("=" * 80)
    print("Testing Weather API with Coordinates")
    print("=" * 80)
    
    # Test 1: Taipei City Hall area
    print("\n📍 Test 1: Taipei City Hall (台北市政府)")
    lat, lng = 25.0408, 121.5674
    
    response = requests.get(f"{BASE_URL}/weather", params={
        "location": "臺北市",
        "lat": lat,
        "lng": lng,
        "include_aqi": "true"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Location: {data['location']}")
        print(f"   Coordinates: ({lat}, {lng})")
        
        weather = data.get('weather', {})
        print(f"\n🌤️  Weather:")
        print(f"   Temperature: {weather.get('temperature')}")
        print(f"   Condition: {weather.get('weather_condition')}")
        print(f"   Rain Prob (3h): {weather.get('rain_probability_3h')}")
        
        aqi = data.get('aqi', {})
        print(f"\n💨 AQI (Nearest Station):")
        print(f"   Site: {aqi.get('site_name')}")
        print(f"   County: {aqi.get('county')}")
        print(f"   AQI: {aqi.get('aqi')}")
        print(f"   Level: {aqi.get('aqi_level')}")
        print(f"   PM2.5: {aqi.get('pm25')}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    # Test 2: Different location (Taipei 101 area)
    print("\n" + "=" * 80)
    print("\n📍 Test 2: Taipei 101 Area")
    lat, lng = 25.0330, 121.5654
    
    response = requests.get(f"{BASE_URL}/weather", params={
        "location": "臺北市",
        "lat": lat,
        "lng": lng,
        "include_aqi": "true"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Location: {data['location']}")
        print(f"   Coordinates: ({lat}, {lng})")
        
        aqi = data.get('aqi', {})
        print(f"\n💨 AQI (Nearest Station):")
        print(f"   Site: {aqi.get('site_name')}")
        print(f"   County: {aqi.get('county')}")
        print(f"   AQI: {aqi.get('aqi')}")
        print(f"   Level: {aqi.get('aqi_level')}")
    
    # Test 3: Without coordinates (fallback to location name)
    print("\n" + "=" * 80)
    print("\n📍 Test 3: Without Coordinates (Fallback)")
    
    response = requests.get(f"{BASE_URL}/weather", params={
        "location": "臺北市",
        "include_aqi": "true"
    })
    
    if response.status_code == 200:
        data = response.json()
        aqi = data.get('aqi', {})
        print(f"\n💨 AQI (County-based lookup):")
        print(f"   Site: {aqi.get('site_name')}")
        print(f"   County: {aqi.get('county')}")
    
    print("\n" + "=" * 80)
    print("\n✅ Summary:")
    print("   • Provide lat & lng → finds NEAREST AQI monitoring station")
    print("   • No coordinates → falls back to county-based lookup")
    print("   • Uses Haversine formula to calculate distances")
    print("=" * 80)


if __name__ == "__main__":
    print("\nMake sure the Flask server is running on http://127.0.0.1:5000")
    print("Start it with: python app.py\n")
    
    try:
        test_weather_with_coordinates()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server")
        print("Please start the Flask server first: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
