#!/usr/bin/env python3
"""
Test Complete Ride Session Flow with MongoDB
Tests the full lifecycle: start -> update -> finish -> retrieve
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000/api/ride"

def test_ride_session_flow():
    """Test complete ride session lifecycle"""
    
    print("=" * 80)
    print("🚴 Testing Complete Ride Session Flow (MongoDB)")
    print("=" * 80)
    
    user_id = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Test 1: Start a ride session
    print("\n🚀 Test 1: Start Ride Session")
    print("-" * 80)
    
    start_data = {
        "user_id": user_id,
        "start_location": {
            "lat": 25.0408,
            "lng": 121.5674
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/start", json=start_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if response.status_code == 201:
            print("✅ Ride session started successfully")
            ride_id = result.get('ride_id')
        else:
            print("❌ Failed to start ride")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the Flask server running on http://localhost:5000?")
        print("💡 Start it with: python app.py")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Update ride metrics
    print("\n📊 Test 2: Update Ride Metrics")
    print("-" * 80)
    
    update_data = {
        "ride_id": ride_id,
        "distance": 1500,  # 1.5 km
        "speed": 12.5,
        "calories": 75,
        "elevation": 10,
        "current_location": {
            "lat": 25.0428,
            "lng": 121.5694
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/update", json=update_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            print("✅ Ride metrics updated successfully")
        else:
            print("❌ Failed to update ride")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Update again (simulate ongoing ride)
    print("\n📈 Test 3: Update Ride Metrics Again")
    print("-" * 80)
    
    update_data_2 = {
        "ride_id": ride_id,
        "distance": 3000,  # 3 km total
        "speed": 15.0,
        "calories": 150,
        "elevation": 15
    }
    
    try:
        response = requests.post(f"{BASE_URL}/update", json=update_data_2)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Ride metrics updated again")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Get active sessions
    print("\n🔍 Test 4: Get Active Sessions")
    print("-" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/active", params={"user_id": user_id})
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Active sessions: {result.get('count')}")
        
        if result.get('sessions'):
            session = result['sessions'][0]
            print(f"\nCurrent session:")
            print(f"  Distance: {session.get('distance')}m")
            print(f"  Max Speed: {session.get('max_speed')} km/h")
            print(f"  Calories: {session.get('calories')}")
            print(f"  Status: {session.get('status')}")
            print("✅ Active session retrieved")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Pause ride
    print("\n⏸️  Test 5: Pause Ride Session")
    print("-" * 80)
    
    try:
        response = requests.post(f"{BASE_URL}/pause", json={"ride_id": ride_id})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Ride paused successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Resume ride
    print("\n▶️  Test 6: Resume Ride Session")
    print("-" * 80)
    
    try:
        response = requests.post(f"{BASE_URL}/resume", json={"ride_id": ride_id})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Ride resumed successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 7: Finish ride
    print("\n🏁 Test 7: Finish Ride Session")
    print("-" * 80)
    
    finish_data = {
        "ride_id": ride_id,
        "end_location": {
            "lat": 25.0448,
            "lng": 121.5714
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/finish", json=finish_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if response.status_code == 200:
            summary = result.get('summary', {})
            print(f"\n🎉 Ride Completed!")
            print(f"  Duration: {summary.get('duration_minutes')} minutes")
            print(f"  Distance: {summary.get('distance_km')} km")
            print(f"  Avg Speed: {summary.get('avg_speed_kmh')} km/h")
            print(f"  Max Speed: {summary.get('max_speed_kmh')} km/h")
            print(f"  Calories: {summary.get('calories')}")
            print(f"  Carbon Saved: {summary.get('carbon_saved_kg')} kg")
            print("✅ Ride finished successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 8: Get ride history
    print("\n📚 Test 8: Get Ride History")
    print("-" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/rides", params={"user_id": user_id})
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Total rides in history: {result.get('count')}")
        
        if result.get('rides'):
            ride = result['rides'][0]
            print(f"\nCompleted ride:")
            print(f"  Duration: {ride.get('duration')}s")
            print(f"  Distance: {ride.get('distance')}m")
            print(f"  Calories: {ride.get('calories')}")
            print("✅ Ride history retrieved")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 9: Get user stats
    print("\n📊 Test 9: Get User Statistics")
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
            print("✅ User stats retrieved")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 10: Verify no active sessions
    print("\n🔍 Test 10: Verify No Active Sessions")
    print("-" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/active", params={"user_id": user_id})
        result = response.json()
        
        if result.get('count') == 0:
            print("✅ No active sessions (session properly closed)")
        else:
            print(f"⚠️  Still has {result.get('count')} active session(s)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 Complete Ride Session Flow Test Complete!")
    print("=" * 80)
    print(f"\n💡 Test user ID: {user_id}")
    print("💡 Check MongoDB Atlas to see both active_sessions and rides collections")
    print("💡 Active session should be moved to rides collection after finishing")


if __name__ == "__main__":
    test_ride_session_flow()
