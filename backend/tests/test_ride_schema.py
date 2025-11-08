#!/usr/bin/env python3
"""
Test Ride Schema - Verify preferred schema format
Tests that rides are saved with correct data types and structure
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api/ride"

def test_ride_schema():
    """Test ride schema matches preferred format"""
    
    print("=" * 80)
    print("📋 Testing Preferred Ride Schema")
    print("=" * 80)
    
    user_id = f"schema_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Test: Save a ride with proper schema
    print("\n💾 Saving ride with preferred schema...")
    print("-" * 80)
    
    ride_data = {
        "user_id": user_id,
        "start_time": "2025-11-08T14:00:00",
        "end_time": "2025-11-08T14:45:00",
        "duration": 2700,  # int - 45 minutes in seconds
        "distance": 8000,  # int - 8 km in meters
        "calories": 400,  # int
        "avg_speed": 10.67,  # float - km/h
        "max_speed": 15.5,  # float - km/h
        "route": [
            {"lat": 25.0408, "lng": 121.5674, "timestamp": "2025-11-08T14:00:00"},
            {"lat": 25.0428, "lng": 121.5694, "timestamp": "2025-11-08T14:15:00"},
            {"lat": 25.0448, "lng": 121.5714, "timestamp": "2025-11-08T14:30:00"},
            {"lat": 25.0468, "lng": 121.5734, "timestamp": "2025-11-08T14:45:00"}
        ],
        "start_location": {
            "lat": 25.0408,
            "lng": 121.5674
        },
        "end_location": {
            "lat": 25.0468,
            "lng": 121.5734
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
        
        if response.status_code == 201:
            print("✅ Ride saved successfully")
            ride_id = result.get('ride_id')
            print(f"   Ride ID: {ride_id}")
        else:
            print(f"❌ Failed: {result}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the Flask server running?")
        print("💡 Start it with: python app.py")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Retrieve and verify schema
    print("\n🔍 Retrieving ride to verify schema...")
    print("-" * 80)
    
    try:
        response = requests.get(f"{BASE_URL}/rides/{ride_id}", params={"user_id": user_id})
        
        if response.status_code == 200:
            ride = response.json().get('ride')
            
            print("\n📋 Retrieved Ride Schema:")
            print(json.dumps(ride, indent=2, ensure_ascii=False))
            
            # Verify data types
            print("\n✓ Schema Verification:")
            checks = []
            
            # Check types
            if isinstance(ride.get('duration'), int):
                checks.append(("✅", "duration", "int", ride['duration']))
            else:
                checks.append(("❌", "duration", f"Expected int, got {type(ride.get('duration')).__name__}", ride.get('duration')))
            
            if isinstance(ride.get('distance'), int):
                checks.append(("✅", "distance", "int", ride['distance']))
            else:
                checks.append(("❌", "distance", f"Expected int, got {type(ride.get('distance')).__name__}", ride.get('distance')))
            
            if isinstance(ride.get('calories'), int):
                checks.append(("✅", "calories", "int", ride['calories']))
            else:
                checks.append(("❌", "calories", f"Expected int, got {type(ride.get('calories')).__name__}", ride.get('calories')))
            
            if isinstance(ride.get('avg_speed'), (int, float)):
                checks.append(("✅", "avg_speed", "float", ride['avg_speed']))
            else:
                checks.append(("❌", "avg_speed", f"Expected float, got {type(ride.get('avg_speed')).__name__}", ride.get('avg_speed')))
            
            if isinstance(ride.get('max_speed'), (int, float)):
                checks.append(("✅", "max_speed", "float", ride['max_speed']))
            else:
                checks.append(("❌", "max_speed", f"Expected float, got {type(ride.get('max_speed')).__name__}", ride.get('max_speed')))
            
            if isinstance(ride.get('route'), list) and len(ride['route']) > 0:
                checks.append(("✅", "route", "array", f"{len(ride['route'])} points"))
            else:
                checks.append(("❌", "route", "Expected array with points", ride.get('route')))
            
            if isinstance(ride.get('start_station'), dict) and 'name' in ride['start_station']:
                checks.append(("✅", "start_station", "object", ride['start_station']['name']))
            else:
                checks.append(("⚠️ ", "start_station", "Optional object", ride.get('start_station')))
            
            if isinstance(ride.get('end_location'), dict) and 'lat' in ride['end_location']:
                checks.append(("✅", "end_location", "GPS object", f"{ride['end_location']['lat']}, {ride['end_location']['lng']}"))
            else:
                checks.append(("❌", "end_location", "Expected GPS object {lat, lng}", ride.get('end_location')))
            
            if isinstance(ride.get('weather'), dict):
                checks.append(("✅", "weather", "object", f"{len(ride['weather'])} fields"))
            else:
                checks.append(("⚠️ ", "weather", "Optional object", ride.get('weather')))
            
            # Print all checks
            print()
            for icon, field, check_type, value in checks:
                print(f"{icon} {field:20} : {check_type:20} = {value}")
            
            # Summary
            success_count = sum(1 for check in checks if check[0] == "✅")
            total_count = len(checks)
            
            print()
            print("=" * 80)
            if success_count == total_count:
                print(f"🎉 All checks passed! ({success_count}/{total_count})")
                print("✅ Ride schema matches preferred format")
            else:
                print(f"⚠️  {success_count}/{total_count} checks passed")
                print("Some fields don't match expected schema")
            print("=" * 80)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test with complete ride session flow
    print("\n\n" + "=" * 80)
    print("🚴 Testing Complete Session Flow with Schema")
    print("=" * 80)
    
    # Start a ride
    print("\n🚀 Starting ride session...")
    start_data = {
        "user_id": user_id,
        "start_location": {"lat": 25.0408, "lng": 121.5674},
        "start_station": {"name": "信義廣場站", "sno": "500101003"}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/start", json=start_data)
        if response.status_code == 201:
            session_ride_id = response.json()['ride_id']
            print(f"✅ Session started: {session_ride_id}")
            
            # Update with location (adds to route)
            print("\n📍 Adding GPS points to route...")
            for i, point in enumerate([
                {"lat": 25.0420, "lng": 121.5680},
                {"lat": 25.0435, "lng": 121.5695},
                {"lat": 25.0450, "lng": 121.5710}
            ], 1):
                update_data = {
                    "ride_id": session_ride_id,
                    "current_location": point,
                    "distance": i * 1000,
                    "speed": 12.0 + i,
                    "calories": i * 50
                }
                response = requests.post(f"{BASE_URL}/update", json=update_data)
                if response.status_code == 200:
                    print(f"  ✅ Point {i} added to route")
            
            # Finish ride
            print("\n🏁 Finishing ride...")
            finish_data = {
                "ride_id": session_ride_id,
                "end_location": {"lat": 25.0468, "lng": 121.5734},
                "weather": {
                    "temperature": "23°C",
                    "condition": "晴",
                    "aqi": "38"
                }
            }
            response = requests.post(f"{BASE_URL}/finish", json=finish_data)
            if response.status_code == 200:
                print("✅ Ride finished and saved to MongoDB")
                
                # Retrieve and check
                print("\n🔍 Checking saved ride from session...")
                response = requests.get(f"{BASE_URL}/rides", params={"user_id": user_id})
                if response.status_code == 200:
                    rides = response.json().get('rides', [])
                    latest_ride = rides[0] if rides else None
                    
                    if latest_ride:
                        route = latest_ride.get('route', [])
                        start_station = latest_ride.get('start_station') or {}
                        end_location = latest_ride.get('end_location')
                        weather = latest_ride.get('weather')
                        
                        print(f"   ✅ Route has {len(route)} GPS points")
                        print(f"   ✅ Start station: {start_station.get('name', 'N/A')}")
                        print(f"   ✅ End location: {end_location}")
                        print(f"   ✅ Weather: {weather}")
                    else:
                        print("   ⚠️  No rides found in history")
                        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("✅ Schema Test Complete!")
    print("=" * 80)
    print(f"💡 Test user: {user_id}")
    print("💡 Check MongoDB Atlas to see the rides with correct schema")


if __name__ == "__main__":
    test_ride_schema()
