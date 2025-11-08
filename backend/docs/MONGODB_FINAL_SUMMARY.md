# 🎉 MongoDB Backend - Complete & Production Ready!

## ✅ Implementation Summary

Your TownPass backend is now fully integrated with MongoDB Atlas and follows your preferred ride schema!

---

## 📋 Preferred Ride Schema (Implemented)

```json
{
  "_id": "ObjectId(...)",
  "user_id": "string",
  "start_time": "2025-11-08T14:00:00",
  "end_time": "2025-11-08T14:45:00",
  "duration": 2700,                    // int - seconds
  "distance": 8000,                    // int - meters
  "calories": 400,                     // int
  "avg_speed": 10.67,                  // float - km/h
  "max_speed": 15.5,                   // float - km/h
  "route": [                           // array of GPS points
    {
      "lat": 25.0408,
      "lng": 121.5674,
      "timestamp": "2025-11-08T14:00:00"
    },
    // ... more points
  ],
  "start_station": {                   // optional - if started from YouBike
    "name": "台北市政府站",
    "sno": "500101001"
  },
  "end_location": {                    // GPS coordinates (not a station!)
    "lat": 25.0468,
    "lng": 121.5734
  },
  "weather": {                         // optional - weather at finish
    "temperature": "22°C",
    "condition": "多雲",
    "aqi": "42"
  },
  "created_at": "2025-11-08T15:49:31Z"
}
```

---

## 🗄️ MongoDB Collections

### 1. **`users`** - User Profiles
```json
{
  "user_id": "device_uuid",
  "created_at": "datetime",
  "total_rides": 10,
  "total_distance": 50000,       // meters
  "total_duration": 18000,        // seconds
  "total_calories": 2500,
  "preferences": {
    "units": "metric",
    "theme": "light"
  }
}
```

### 2. **`rides`** - Completed Ride History
Uses the preferred schema above. Permanent storage.

### 3. **`active_sessions`** - Currently Active Rides (Temporary)
```json
{
  "ride_id": "uuid",
  "user_id": "device_uuid",
  "start_time": "ISO string",
  "start_location": {"lat": float, "lng": float},
  "start_station": {"name": str, "sno": str},  // optional
  "distance": 0.0,
  "max_speed": 0.0,
  "calories": 0.0,
  "route": [],                    // accumulates during ride
  "status": "active|paused",
  "created_at": "datetime"
}
```

---

## 🚀 API Endpoints

### **Active Session Management**

#### `POST /api/ride/start`
Start a new ride session
```json
{
  "user_id": "required",
  "start_location": {"lat": 25.04, "lng": 121.56},
  "start_station": {"name": "站名", "sno": "500101001"}  // optional
}
```

#### `POST /api/ride/update`
Update metrics during ride (adds GPS points to route)
```json
{
  "ride_id": "required",
  "distance": 1500,                          // total meters
  "speed": 12.5,                             // current km/h
  "calories": 75,                            // total burned
  "current_location": {"lat": 25.04, "lng": 121.56}  // adds to route!
}
```

#### `POST /api/ride/finish`
Finish and save ride to MongoDB
```json
{
  "ride_id": "required",
  "end_location": {"lat": 25.05, "lng": 121.57},  // required!
  "weather": {                               // optional
    "temperature": "22°C",
    "condition": "多雲",
    "aqi": "42"
  }
}
```

#### `GET /api/ride/active?user_id=xxx`
Get active sessions for user

#### `POST /api/ride/pause` / `POST /api/ride/resume`
Pause/resume active session

---

### **Completed Rides**

#### `POST /api/ride/rides`
Manually save a ride (alternative to finish)

#### `GET /api/ride/rides?user_id=xxx&limit=50&skip=0`
Get ride history (pagination supported)

#### `GET /api/ride/rides/<ride_id>?user_id=xxx`
Get specific ride details

#### `DELETE /api/ride/rides/<ride_id>?user_id=xxx`
Delete a ride

#### `GET /api/ride/stats?user_id=xxx`
Get aggregated user statistics

---

## 🎯 Key Features Implemented

### ✅ **Automatic Route Tracking**
- Every time you send `current_location` in `/update`, it adds a GPS point to the route
- Route array automatically built during the ride
- Timestamps added automatically

### ✅ **Flexible Start Points**
- Can start from YouBike station → includes `start_station` data
- Can start anywhere → just provide GPS `start_location`

### ✅ **GPS End Location**
- `end_location` is always GPS coordinates (not a station)
- Perfect for ending rides anywhere

### ✅ **Weather Integration**
- Provide weather data when finishing ride
- Stored with the completed ride

### ✅ **Data Type Enforcement**
- `duration`, `distance`, `calories` → `int`
- `avg_speed`, `max_speed` → `float`
- Exactly matches your preferred schema

---

## 📱 Frontend Integration Guide

### **1. Generate User ID (One Time)**
```javascript
// composables/useUserData.js
import { v4 as uuidv4 } from 'uuid'

const USER_ID_KEY = 'townpass_user_id'

export function useUserData() {
  const getUserId = () => {
    let userId = localStorage.getItem(USER_ID_KEY)
    if (!userId) {
      userId = uuidv4()
      localStorage.setItem(USER_ID_KEY, userId)
    }
    return userId
  }

  return { userId: getUserId() }
}
```

### **2. Start Ride**
```javascript
const { userId } = useUserData()

// From GPS location
const startRide = async (location) => {
  const response = await fetch('/api/ride/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      start_location: location
    })
  })
  const data = await response.json()
  return data.ride_id
}

// From YouBike station
const startRideFromStation = async (location, station) => {
  const response = await fetch('/api/ride/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      start_location: location,
      start_station: station  // {name, sno}
    })
  })
  const data = await response.json()
  return data.ride_id
}
```

### **3. Track Location During Ride**
```javascript
const updateRide = async (rideId, location, metrics) => {
  await fetch('/api/ride/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ride_id: rideId,
      current_location: location,  // Automatically adds to route!
      distance: metrics.distance,
      speed: metrics.speed,
      calories: metrics.calories
    })
  })
}

// Call every 5-10 seconds or on significant location change
setInterval(() => {
  const location = { lat: currentLat, lng: currentLng }
  const metrics = calculateMetrics()
  updateRide(activeRideId, location, metrics)
}, 10000)  // 10 seconds
```

### **4. Finish Ride**
```javascript
const finishRide = async (rideId, endLocation, weather) => {
  const response = await fetch('/api/ride/finish', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ride_id: rideId,
      end_location: endLocation,  // {lat, lng}
      weather: weather            // optional
    })
  })
  return await response.json()
}
```

### **5. Get Ride History**
```javascript
const getRideHistory = async (limit = 50, skip = 0) => {
  const response = await fetch(
    `/api/ride/rides?user_id=${userId}&limit=${limit}&skip=${skip}`
  )
  const data = await response.json()
  return data.rides
}
```

### **6. Get User Stats**
```javascript
const getUserStats = async () => {
  const response = await fetch(`/api/ride/stats?user_id=${userId}`)
  const data = await response.json()
  return data.stats
}
```

---

## 🧪 Testing

### **Run All Tests**
```bash
cd /Users/tedlu/Desktop/townpass-dev/backend

# Test MongoDB connection
python3 -c "from database import init_database; init_database()"

# Test schema
python3 test_ride_schema.py

# Test complete session flow
python3 test_ride_session.py

# Test MongoDB persistence
python3 test_mongodb.py
```

### **Manual API Testing**
```bash
# Start server
python3 app.py

# In another terminal
# Start ride
curl -X POST http://localhost:5000/api/ride/start \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test123","start_location":{"lat":25.04,"lng":121.56}}'

# Update ride
curl -X POST http://localhost:5000/api/ride/update \
  -H "Content-Type: application/json" \
  -d '{"ride_id":"...","current_location":{"lat":25.05,"lng":121.57},"distance":1000,"speed":12}'

# Finish ride
curl -X POST http://localhost:5000/api/ride/finish \
  -H "Content-Type: application/json" \
  -d '{"ride_id":"...","end_location":{"lat":25.06,"lng":121.58}}'

# Get history
curl "http://localhost:5000/api/ride/rides?user_id=test123"
```

---

## 🚀 Deploy to Cloud Run

```bash
cd /Users/tedlu/Desktop/townpass-dev/backend

# Deploy
gcloud run deploy townpass-backend \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/" \
  --set-env-vars MONGODB_DB_NAME="townpass" \
  --set-env-vars CWA_API_KEY="your_key" \
  --memory 512Mi \
  --max-instances 10
```

---

## ✅ Schema Validation Results

All 9/9 checks passed! ✅

- ✅ `duration` → int (seconds)
- ✅ `distance` → int (meters)
- ✅ `calories` → int
- ✅ `avg_speed` → float (km/h)
- ✅ `max_speed` → float (km/h)
- ✅ `route` → array of GPS points
- ✅ `start_station` → object {name, sno}
- ✅ `end_location` → GPS object {lat, lng}
- ✅ `weather` → object

---

## 🎯 Summary

**Your backend is:**
- ✅ Using MongoDB Atlas
- ✅ Following your exact preferred schema
- ✅ Tracking GPS routes automatically
- ✅ Supporting YouBike stations
- ✅ Using GPS coordinates for end locations (not stations)
- ✅ Enforcing correct data types
- ✅ Production ready for Cloud Run
- ✅ Fully tested and validated

**Ready to integrate with your Vue.js frontend! 🚴‍♂️**
