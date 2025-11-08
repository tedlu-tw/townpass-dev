#!/usr/bin/env python3
"""
Test script for ride API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api/ride"

def test_start_ride():
    """Test starting a ride"""
    print("\n1. Testing ride start...")
    data = {
        "user_id": "test_user_123",
        "start_location": {
            "lat": 25.0330,
            "lng": 121.5654
        }
    }
    
    response = requests.post(f"{BASE_URL}/start", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        ride_id = response.json().get('ride_id')
        print(f"✅ Ride started with ID: {ride_id}")
        return ride_id
    else:
        print(f"❌ Failed to start ride")
        return None

def test_update_ride(ride_id):
    """Test updating ride metrics"""
    print(f"\n2. Testing ride update...")
    
    # Simulate movement
    locations = [
        {"lat": 25.0331, "lng": 121.5655},
        {"lat": 25.0332, "lng": 121.5656},
        {"lat": 25.0333, "lng": 121.5657}
    ]
    
    for i, loc in enumerate(locations):
        data = {
            "ride_id": ride_id,
            "current_location": loc,
            "speed": 15.5 + i * 0.5  # Increasing speed
        }
        
        response = requests.post(f"{BASE_URL}/update", json=data)
        print(f"Update {i+1} - Status: {response.status_code}")
        
        if response.status_code == 200:
            updated = response.json().get('updated_fields', {})
            print(f"  Distance added: {updated.get('distance_added', 0):.2f}m")
            print(f"  Calories: {updated.get('calories', 0):.2f}")
        
        time.sleep(1)  # Wait 1 second between updates

def test_get_status(ride_id):
    """Test getting ride status"""
    print(f"\n3. Testing ride status...")
    
    response = requests.get(f"{BASE_URL}/status", params={"ride_id": ride_id})
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        status = response.json()
        print(f"Response: {json.dumps(status, indent=2)}")
        print(f"\n📊 Ride Metrics:")
        print(f"  Duration: {status.get('duration_seconds')}s")
        print(f"  Distance: {status.get('distance_km'):.3f} km")
        print(f"  Avg Speed: {status.get('avg_speed_kmh'):.1f} km/h")
        print(f"  Calories: {status.get('calories'):.1f} kcal")
        print(f"  Route points: {status.get('route_points')}")
    else:
        print(f"Response: {response.json()}")

def test_finish_ride(ride_id):
    """Test finishing a ride"""
    print(f"\n4. Testing ride finish...")
    
    data = {
        "ride_id": ride_id,
        "end_location": {
            "lat": 25.0333,
            "lng": 121.5657
        },
        "weather": {
            "temperature": "24°C",
            "condition": "Sunny",
            "aqi": "Good"
        }
    }
    
    response = requests.post(f"{BASE_URL}/finish", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Ride finished!")
        print(f"Summary: {json.dumps(result.get('summary'), indent=2)}")
    else:
        print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚴 Testing Ride API Endpoints")
    print("=" * 60)
    
    # Test ride session
    ride_id = test_start_ride()
    
    if ride_id:
        time.sleep(2)  # Wait 2 seconds
        test_update_ride(ride_id)
        time.sleep(2)  # Wait 2 seconds
        test_get_status(ride_id)
        time.sleep(1)  # Wait 1 second
        test_finish_ride(ride_id)
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")
    print("=" * 60)
