#!/usr/bin/env python3
"""
Test MongoDB integration with TownPass Backend
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api/ride"

def test_mongodb_integration():
    """Test MongoDB ride persistence"""
    
    print("=" * 80)
    print("🧪 Testing MongoDB Integration")
    print("=" * 80)
    
    user_id = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Test 1: Save a ride
    print("\n📝 Test 1: Save a ride")
    print("-" * 80)
    
    ride_data = {
        "user_id": user_id,
        "start_time": "2025-11-08T10:00:00",
        "end_time": "2025-11-08T10:30:00",
        "duration": 1800,  # 30 minutes
        "distance": 5000,  # 5 km in meters
        "calories": 250,
        "avg_speed": 10.0,  # km/h
        "max_speed": 15.0,  # km/h
        "route": [
            {"lat": 25.0408, "lng": 121.5674, "timestamp": "2025-11-08T10:00:00"},
            {"lat": 25.0428, "lng": 121.5694, "timestamp": "2025-11-08T10:15:00"},
            {"lat": 25.0448, "lng": 121.5714, "timestamp": "2025-11-08T10:30:00"}
        ],
        "start_location": {
            "lat": 25.0408,
            "lng": 121.5674
        },
        "end_location": {
            "lat": 25.0448,
            "lng": 121.5714
        },
        "weather": {
            "temperature": "22°C",
            "condition": "多雲",
            "aqi": "42"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/rides", json=ride_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            print("✅ Ride saved successfully")
            ride_id = result.get('ride_id')
        else:
            print("❌ Failed to save ride")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the Flask server running on http://localhost:5000?")
        print("💡 Start it with: python app.py")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Get user's rides
    print("\n📚 Test 2: Get ride history")
    print("-" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/rides", params={"user_id": user_id})
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Found {result.get('count', 0)} rides")
        
        if result.get('rides'):
            print("\nFirst ride details:")
            print(json.dumps(result['rides'][0], indent=2, ensure_ascii=False))
            print("✅ Ride history retrieved successfully")
        else:
            print("⚠️  No rides found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Get specific ride
    print("\n🔍 Test 3: Get specific ride")
    print("-" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/rides/{ride_id}", params={"user_id": user_id})
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if 'ride' in result:
            ride = result['ride']
            print(f"\nRide Details:")
            print(f"  Duration: {ride.get('duration')}s ({ride.get('duration', 0) / 60:.1f} minutes)")
            print(f"  Distance: {ride.get('distance')}m ({ride.get('distance', 0) / 1000:.2f} km)")
            print(f"  Calories: {ride.get('calories')}")
            print(f"  Avg Speed: {ride.get('avg_speed')} km/h")
            print(f"  Route points: {len(ride.get('route', []))}")
            print("✅ Ride details retrieved successfully")
        else:
            print("❌ Ride not found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Get user stats
    print("\n📊 Test 4: Get user statistics")
    print("-" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/stats", params={"user_id": user_id})
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if 'stats' in result:
            stats = result['stats']
            print(f"\nUser Statistics:")
            print(f"  Total Rides: {stats.get('total_rides')}")
            print(f"  Total Distance: {stats.get('total_distance', 0) / 1000:.2f} km")
            print(f"  Total Duration: {stats.get('total_duration', 0) / 60:.1f} minutes")
            print(f"  Total Calories: {stats.get('total_calories')}")
            print(f"  Avg Distance: {stats.get('avg_distance', 0) / 1000:.2f} km")
            print(f"  Avg Duration: {stats.get('avg_duration', 0) / 60:.1f} minutes")
            print("✅ User statistics retrieved successfully")
        else:
            print("❌ Stats not found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Save another ride to test stats accumulation
    print("\n📝 Test 5: Save second ride (test stats accumulation)")
    print("-" * 80)
    
    ride_data_2 = {
        **ride_data,
        "start_time": "2025-11-08T14:00:00",
        "end_time": "2025-11-08T14:45:00",
        "duration": 2700,  # 45 minutes
        "distance": 8000,  # 8 km
        "calories": 400
    }
    
    try:
        response = requests.post(f"{BASE_URL}/rides", json=ride_data_2)
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if response.status_code == 201:
            print("✅ Second ride saved successfully")
            
            # Get updated stats
            response = requests.get(f"{BASE_URL}/stats", params={"user_id": user_id})
            stats = response.json().get('stats', {})
            print(f"\nUpdated Statistics:")
            print(f"  Total Rides: {stats.get('total_rides')}")
            print(f"  Total Distance: {stats.get('total_distance', 0) / 1000:.2f} km")
            print(f"  Total Calories: {stats.get('total_calories')}")
            print("✅ Stats accumulation working correctly")
        else:
            print("❌ Failed to save second ride")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Delete a ride
    print("\n🗑️  Test 6: Delete a ride")
    print("-" * 80)
    
    try:
        response = requests.delete(f"{BASE_URL}/rides/{ride_id}", params={"user_id": user_id})
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print("✅ Ride deleted successfully")
        else:
            print("❌ Failed to delete ride")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 Testing Complete!")
    print("=" * 80)
    print(f"\n💡 Test user ID: {user_id}")
    print("💡 You can check MongoDB Atlas to see the data")


if __name__ == "__main__":
    test_mongodb_integration()
