#!/usr/bin/env python3
"""
Test script for TownPass Backend API
Demonstrates all major endpoints
"""

import requests
import json
import time
from typing import Dict

BASE_URL = "http://127.0.0.1:5000"


def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*80}")
    print(f"🧪 {title}")
    print(f"{'='*80}")
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_ride_flow(user_id: str = "test_user_001"):
    """Test complete ride flow: start -> update -> finish"""
    
    # 1. Start a ride
    print("\n" + "🚴 Starting Ride Flow Test".center(80, "="))
    
    start_data = {
        "user_id": user_id,
        "start_location": {"lat": 25.0330, "lng": 121.5654}
    }
    response = requests.post(f"{BASE_URL}/api/ride/start", json=start_data)
    print_response("1. Start Ride", response)
    
    if response.status_code != 201:
        print("❌ Failed to start ride")
        return None
    
    ride_id = response.json()["ride_id"]
    print(f"\n✅ Ride started with ID: {ride_id}")
    
    # 2. Update ride metrics (simulate riding)
    time.sleep(1)
    
    update_data = {
        "ride_id": ride_id,
        "distance": 1500,  # meters
        "speed": 15.5,     # km/h
        "calories": 45,
        "paused_time": 0,
        "elevation": 10
    }
    response = requests.post(f"{BASE_URL}/api/ride/update", json=update_data)
    print_response("2. Update Ride (First Update)", response)
    
    # 3. Update again (more distance)
    time.sleep(1)
    
    update_data = {
        "ride_id": ride_id,
        "distance": 3500,
        "speed": 18.2,
        "calories": 125,
        "paused_time": 60,
        "elevation": 15
    }
    response = requests.post(f"{BASE_URL}/api/ride/update", json=update_data)
    print_response("3. Update Ride (Second Update)", response)
    
    # 4. Finish the ride
    time.sleep(1)
    
    finish_data = {
        "ride_id": ride_id,
        "end_location": {"lat": 25.0450, "lng": 121.5780}
    }
    response = requests.post(f"{BASE_URL}/api/ride/finish", json=finish_data)
    print_response("4. Finish Ride", response)
    
    return ride_id


def test_history(ride_id: str = None, user_id: str = "test_user_001"):
    """Test history endpoints"""
    print("\n" + "📚 Testing History Endpoints".center(80, "="))
    
    # Get all history
    response = requests.get(f"{BASE_URL}/api/history", params={"user_id": user_id})
    print_response("1. Get All History", response)
    
    # Get specific ride
    if ride_id:
        response = requests.get(f"{BASE_URL}/api/history/{ride_id}")
        print_response("2. Get Specific Ride", response)


def test_stations():
    """Test station endpoints"""
    print("\n" + "🚉 Testing Station Endpoints".center(80, "="))
    
    # Get nearby stations (Taipei City Hall area)
    params = {
        "lat": 25.0408,
        "lng": 121.5674,
        "radius": 1000,
        "limit": 5
    }
    response = requests.get(f"{BASE_URL}/api/station/nearby", params=params)
    print_response("1. Get Nearby Stations", response)
    
    # Get station stats
    response = requests.get(f"{BASE_URL}/api/station/stats")
    print_response("2. Get Station Statistics", response)
    
    # Get available stations
    response = requests.get(f"{BASE_URL}/api/station/available", params={"min_bikes": 3, "limit": 5})
    print_response("3. Get Available Stations", response)


def test_weather():
    """Test weather endpoints"""
    print("\n" + "🌤️ Testing Weather Endpoints".center(80, "="))
    
    # Get weather and AQI
    params = {"location": "臺北市", "include_aqi": "true"}
    response = requests.get(f"{BASE_URL}/api/weather", params=params)
    print_response("1. Get Weather & AQI", response)
    
    # Get AQI status
    response = requests.get(f"{BASE_URL}/api/aqi/status")
    print_response("2. Get AQI Status", response)


def test_stats(user_id: str = "test_user_001"):
    """Test statistics endpoints"""
    print("\n" + "📊 Testing Statistics Endpoints".center(80, "="))
    
    # Get user stats
    response = requests.get(f"{BASE_URL}/api/stats", params={"user_id": user_id})
    print_response("1. Get User Statistics", response)
    
    # Get leaderboard
    response = requests.get(f"{BASE_URL}/api/stats/leaderboard", params={"metric": "distance", "limit": 5})
    print_response("2. Get Leaderboard", response)
    
    # Get achievements
    response = requests.get(f"{BASE_URL}/api/stats/achievements", params={"user_id": user_id})
    print_response("3. Get Achievements", response)


def run_all_tests():
    """Run all API tests"""
    print("\n" + "🧪 TownPass Backend API Test Suite".center(80, "="))
    print("Testing all endpoints...")
    
    user_id = "test_user_001"
    
    try:
        # Test health check
        if not test_health_check():
            print("\n❌ Server is not healthy. Please start the server first.")
            return
        
        # Test ride flow
        ride_id = test_ride_flow(user_id)
        
        # Test history
        test_history(ride_id, user_id)
        
        # Test stations
        test_stations()
        
        # Test weather
        test_weather()
        
        # Test stats
        test_stats(user_id)
        
        print("\n" + "✅ All Tests Completed!".center(80, "="))
        print("\n📝 Summary:")
        print("  ✓ Health Check")
        print("  ✓ Ride Management (Start → Update → Finish)")
        print("  ✓ History Tracking")
        print("  ✓ Station Information")
        print("  ✓ Weather & AQI")
        print("  ✓ Statistics & Achievements")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server")
        print("Please ensure the Flask server is running:")
        print("  python app.py")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")


if __name__ == "__main__":
    print("\n" + "TownPass Backend API Test".center(80, "="))
    print("Make sure the Flask server is running on http://127.0.0.1:5000")
    print("Start it with: python app.py")
    print("="*80)
    
    input("\nPress Enter to start testing...")
    
    run_all_tests()
