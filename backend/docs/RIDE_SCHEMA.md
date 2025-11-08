# 🚴 Ride Schema Documentation

## 📋 Complete Ride Schema

This is the **preferred and implemented** ride schema for the TownPass cycling backend.

### Schema Overview

```json
{
  "_id": ObjectId("..."),
  "user_id": "string",
  "start_time": "2025-11-08T14:00:00",
  "end_time": "2025-11-08T14:45:00",
  "duration": 2700,                    // int - active riding time in seconds
  "distance": 8000,                    // int - total distance in meters
  "calories": 400,                     // int - calories burned
  "avg_speed": 10.67,                  // float - average speed in km/h
  "max_speed": 15.5,                   // float - maximum speed in km/h
  "route": [                           // array of GPS tracking points
    {
      "lat": 25.0408,                  // float - latitude
      "lng": 121.5674,                 // float - longitude
      "timestamp": "2025-11-08T14:00:00"  // ISO timestamp
    },
    {
      "lat": 25.0428,
      "lng": 121.5694,
      "timestamp": "2025-11-08T14:15:00"
    }
    // ... more GPS points tracked during ride
  ],
  "start_location": {                  // REQUIRED - GPS coordinates where ride started
    "lat": 25.0408,                    // float - initial latitude
    "lng": 121.5674                    // float - initial longitude
  },
  "end_location": {                    // REQUIRED - GPS coordinates where ride ended
    "lat": 25.0468,                    // float - final latitude
    "lng": 121.5734                    // float - final longitude
  },
  "weather": {                         // OPTIONAL - weather conditions at ride completion
    "temperature": "22°C",
    "condition": "多雲",
    "aqi": "42"
  },
  "created_at": ISODate("2025-11-08T15:49:31.678Z")  // timestamp when saved to DB
}
```

---

## 🔑 Field Specifications

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `user_id` | string | Unique user identifier (device UUID) | `"device_abc123"` |
| `start_time` | string (ISO) | When ride started | `"2025-11-08T14:00:00"` |
| `end_time` | string (ISO) | When ride ended | `"2025-11-08T14:45:00"` |
| `duration` | int | Active riding time (seconds) | `2700` (45 min) |
| `distance` | int | Total distance (meters) | `8000` (8 km) |
| `calories` | int | Calories burned | `400` |
| `avg_speed` | float | Average speed (km/h) | `10.67` |
| `max_speed` | float | Maximum speed (km/h) | `15.5` |
| `route` | array | GPS tracking points | `[{lat, lng, timestamp}, ...]` |
| `start_location` | object | GPS coordinates where ride started | `{lat: 25.04, lng: 121.56}` |
| `end_location` | object | GPS coordinates where ride ended | `{lat: 25.05, lng: 121.57}` |

### Optional Fields

| Field | Type | Description | When to Include |
|-------|------|-------------|-----------------|
| `weather` | object | Weather at completion | Include for better ride context |

---

## 📍 Location Fields Explained

### `start_location` (Required)
- **Purpose**: Records GPS coordinates where ride started
- **Structure**: `{lat: float, lng: float}`
- **Example**: `{lat: 25.0408, lng: 121.5674}`
- **Why GPS**: Users can start rides anywhere (not just at stations)
- **Note**: This is **NOT** a YouBike station - it's a free-form GPS point

### `end_location` (Required)
- **Purpose**: Records GPS coordinates where ride ended
- **Structure**: `{lat: float, lng: float}`
- **Example**: `{lat: 25.0468, lng: 121.5734}`
- **Why GPS**: Users can end rides anywhere (not just at stations)
- **Note**: This is **NOT** a YouBike station - it's a free-form GPS point

### Why Not `end_station`?
❌ **Old/Incorrect**: `end_station: {name, sno}` (assumes ride ends at station)
✅ **Correct**: `end_location: {lat, lng}` (allows ending anywhere)

**Reason**: Users may:
- Park at any location (not just YouBike stations)
- Return bikes to full stations and park nearby
- End rides at their final destination (home, office, etc.)

---

## 🛣️ Route Tracking

The `route` array accumulates GPS points throughout the ride:

### How It Works
1. User starts ride → initial point may be added
2. During ride → `/update` endpoint with `current_location` adds points
3. Points automatically timestamped
4. All points saved when ride finishes

### Route Point Structure
```json
{
  "lat": 25.0428,                    // float - latitude
  "lng": 121.5694,                   // float - longitude  
  "timestamp": "2025-11-08T14:15:00" // ISO string - when point recorded
}
```

### Frontend Usage
```javascript
// Add GPS point during ride
const updateRide = async (rideId, location) => {
  await fetch(`${API_URL}/ride/update`, {
    method: 'POST',
    body: JSON.stringify({
      ride_id: rideId,
      current_location: {
        lat: location.latitude,
        lng: location.longitude
      },
      distance: currentDistance,
      speed: currentSpeed,
      calories: currentCalories
    })
  });
  // Location automatically added to route with timestamp
};
```

---

## 🌤️ Weather Data

Optional but recommended to include weather at ride completion:

```json
{
  "temperature": "22°C",    // string - temperature with unit
  "condition": "多雲",       // string - weather description (localized)
  "aqi": "42"               // string - air quality index
}
```

### How to Get Weather
Use the `/api/weather` endpoint before finishing:

```javascript
// Get weather at current location
const weather = await fetch(
  `${API_URL}/weather?lat=${lat}&lng=${lng}`
).then(r => r.json());

// Finish ride with weather
await fetch(`${API_URL}/ride/finish`, {
  method: 'POST',
  body: JSON.stringify({
    ride_id: rideId,
    end_location: { lat, lng },
    weather: {
      temperature: `${weather.temperature}°C`,
      condition: weather.weather,
      aqi: weather.aqi.value.toString()
    }
  })
});
```

---

## 🔢 Data Type Requirements

**Critical**: Ensure correct data types for MongoDB

| Field | MongoDB Type | JavaScript/JSON | Notes |
|-------|-------------|-----------------|-------|
| `duration` | Int32 | number (int) | Must be whole number |
| `distance` | Int32 | number (int) | Meters as whole number |
| `calories` | Int32 | number (int) | Whole number |
| `avg_speed` | Double | number (float) | Can have decimals |
| `max_speed` | Double | number (float) | Can have decimals |
| `route` | Array | array | Must be array of objects |
| `start_location` | Object | object | Required object |
| `end_location` | Object | object | Required object |
| `weather` | Object | object | Null/empty if not recorded |

### Type Conversion in Backend
The backend automatically handles type conversion:
```python
ride_record = {
    "duration": int(active_duration),           # Float → Int
    "distance": int(session.get('distance', 0)), # Float → Int  
    "calories": int(session.get('calories', 0)), # Float → Int
    "avg_speed": round(avg_speed, 2),            # Keep as float
    "max_speed": float(session.get('max_speed', 0))  # Ensure float
}
```

---

## 📱 Frontend Implementation Examples

### Complete Ride Flow

```javascript
// 1. Start Ride
const startRide = async (userId, location) => {
  const response = await fetch(`${API_URL}/ride/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      start_location: { lat: location.latitude, lng: location.longitude }
    })
  });
  
  const { ride_id } = await response.json();
  return ride_id;
};

// 2. Update During Ride (adds GPS points to route)
const updateRide = async (rideId, metrics) => {
  await fetch(`${API_URL}/ride/update`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ride_id: rideId,
      distance: metrics.totalDistance,      // meters (will be converted to int)
      speed: metrics.currentSpeed,          // km/h
      calories: metrics.caloriesBurned,     // total (will be converted to int)
      current_location: {                   // Adds point to route!
        lat: metrics.currentLat,
        lng: metrics.currentLng
      }
    })
  });
};

// 3. Finish Ride
const finishRide = async (rideId, endLocation, weatherData) => {
  const response = await fetch(`${API_URL}/ride/finish`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ride_id: rideId,
      end_location: {                       // GPS coordinates (NOT a station!)
        lat: endLocation.latitude,
        lng: endLocation.longitude
      },
      weather: {
        temperature: `${weatherData.temp}°C`,
        condition: weatherData.condition,
        aqi: weatherData.aqi.toString()
      }
    })
  });
  
  const { summary } = await response.json();
  return summary;
};
```

---

## ✅ Schema Validation Checklist

Use this checklist to verify your ride data:

- [ ] `duration` is an **integer** (seconds)
- [ ] `distance` is an **integer** (meters)
- [ ] `calories` is an **integer**
- [ ] `avg_speed` is a **float** (km/h)
- [ ] `max_speed` is a **float** (km/h)
- [ ] `route` is an **array** with GPS objects `{lat, lng, timestamp}`
- [ ] `start_location` is an **object** `{lat, lng}` (REQUIRED)
- [ ] `end_location` is an **object** `{lat, lng}` (REQUIRED)
- [ ] `end_location` uses **GPS coordinates**, NOT a station
- [ ] `weather` is an **object** OR **null/omitted**

---

## 🧪 Testing

Run the schema validation test:

```bash
cd backend
python test_ride_schema.py
```

This test will:
1. Save a ride with the preferred schema
2. Retrieve it from MongoDB
3. Verify all data types are correct
4. Test the complete session flow (start → update → finish)
5. Confirm GPS points are added to route
6. Verify end_location uses GPS coordinates

Expected output:
```
✅ All checks passed! (9/9)
✅ Ride schema matches preferred format
✅ Route has 3 GPS points
✅ End location: {lat: 25.0468, lng: 121.5734}
```

---

## 🗄️ MongoDB Storage Example

Actual document in MongoDB Atlas:

```json
{
  "_id": {"$oid": "690f60d764bf3d76400bfb93"},
  "user_id": "test_user_20251108_232510",
  "start_time": "2025-11-08T14:00:00",
  "end_time": "2025-11-08T14:45:00",
  "duration": {"$numberInt": "2700"},
  "distance": {"$numberInt": "8000"},
  "calories": {"$numberInt": "400"},
  "avg_speed": {"$numberDouble": "10.67"},
  "max_speed": {"$numberDouble": "15.5"},
  "route": [
    {
      "lat": {"$numberDouble": "25.0408"},
      "lng": {"$numberDouble": "121.5674"},
      "timestamp": "2025-11-08T14:00:00"
    },
    {
      "lat": {"$numberDouble": "25.0428"},
      "lng": {"$numberDouble": "121.5694"},
      "timestamp": "2025-11-08T14:15:00"
    },
    {
      "lat": {"$numberDouble": "25.0448"},
      "lng": {"$numberDouble": "121.5714"},
      "timestamp": "2025-11-08T14:30:00"
    }
  ],
  "start_location": {
    "lat": {"$numberDouble": "25.0408"},
    "lng": {"$numberDouble": "121.5674"}
  },
  "end_location": {
    "lat": {"$numberDouble": "25.0468"},
    "lng": {"$numberDouble": "121.5734"}
  },
  "weather": {
    "temperature": "22°C",
    "condition": "多雲",
    "aqi": "42"
  },
  "created_at": {"$date": {"$numberLong": "1762615511678"}}
}
```

---

## 📚 Related Documentation

- **API Endpoints**: See `MONGODB_FINAL_SUMMARY.md` for complete endpoint documentation
- **Setup Guide**: See `MONGODB_CLOUDRUN_SETUP.md` for deployment instructions
- **Database Module**: See `database.py` for implementation details
- **Route Handlers**: See `routes/ride_routes.py` for endpoint logic

---

## ❓ FAQ

### Q: Why not use `end_station` like `start_station`?
**A**: Rides can end anywhere, not just at YouBike stations. Users may park at their destination, end at a full station, or simply stop riding. GPS coordinates provide flexibility.

### Q: What if ride starts from a random location (not a station)?
**A**: Include `start_location` with GPS coordinates. The schema handles both cases.

### Q: Should I send GPS updates constantly?
**A**: Recommended: send location updates every 10-30 seconds during active riding. This builds a detailed route without excessive API calls.

### Q: What if weather data is unavailable?
**A**: Weather is optional. You can omit the field or pass an empty object `{}`.

### Q: How do I convert distance from km to meters?
**A**: Multiply by 1000: `distance_meters = distance_km * 1000`

---

**Last Updated**: 2025-11-08  
**Schema Version**: 1.0 (Final)  
**Status**: ✅ Implemented and Tested
