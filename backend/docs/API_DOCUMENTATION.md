# TownPass Backend API

A Flask-based RESTful API backend for the TownPass cycling application. This backend handles ride sessions, history tracking, YouBike station data, weather information, and user statistics.

## 🚀 Features

- **Ride Management**: Start, update, and finish cycling sessions
- **History Tracking**: Store and retrieve ride history
- **Station Information**: Real-time YouBike station availability
- **Weather & AQI**: Current weather and air quality data
- **Statistics**: User performance metrics and achievements

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API Keys (provided in `.env` file):
  - CWA_API_KEY (Central Weather Administration)
  - MOENV_API_KEY (Ministry of Environment)

## 🛠️ Installation

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify `.env` file** (already provided):
   ```bash
   cat .env
   ```
   
   Should contain:
   ```
   CWA_API_KEY=CWA-E55648B2-9676-4603-A8A4-6662D8D488BB
   MOENV_API_KEY=7a1783c1-2016-42b1-8c9c-26ecad517708
   ```

## 🏃 Running the Server

Start the Flask development server:

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000`

You should see:
```
============================================================
🚴 TownPass Backend API Server
============================================================
📍 Server running on: http://127.0.0.1:5000
📖 API Documentation: http://127.0.0.1:5000/
💚 Health Check: http://127.0.0.1:5000/health
============================================================
```

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:5000
```

### Endpoints Overview

#### 1. Ride Management (`/api/ride`)

##### Start a Ride
```http
POST /api/ride/start
Content-Type: application/json

{
  "user_id": "user001",
  "start_location": {"lat": 25.0330, "lng": 121.5654}
}
```

**Response**:
```json
{
  "ride_id": "b8a2c3e1-1234-4567-8901-9a87654d3210",
  "user_id": "user001",
  "start_time": "2025-11-08T10:30:00",
  "message": "Ride session started."
}
```

##### Update Ride Metrics
```http
POST /api/ride/update
Content-Type: application/json

{
  "ride_id": "b8a2c3e1-1234-4567-8901-9a87654d3210",
  "distance": 1500,
  "speed": 15.5,
  "calories": 45,
  "paused_time": 120,
  "elevation": 10
}
```

##### Finish a Ride
```http
POST /api/ride/finish
Content-Type: application/json

{
  "ride_id": "b8a2c3e1-1234-4567-8901-9a87654d3210",
  "end_location": {"lat": 25.0450, "lng": 121.5780}
}
```

**Response**:
```json
{
  "ride_id": "b8a2c3e1-1234-4567-8901-9a87654d3210",
  "message": "Ride session finished successfully.",
  "summary": {
    "duration_minutes": 25.5,
    "distance_km": 5.2,
    "avg_speed_kmh": 12.3,
    "max_speed_kmh": 18.5,
    "calories": 125.4,
    "carbon_saved_kg": 0.624
  }
}
```

#### 2. History (`/api/history`)

##### Get All Rides
```http
GET /api/history?user_id=user001&limit=10&sort=desc
```

##### Get Specific Ride
```http
GET /api/history/{ride_id}
```

##### Delete a Ride
```http
DELETE /api/history/{ride_id}
```

#### 3. Stations (`/api/station`)

##### Get Nearby Stations
```http
GET /api/station/nearby?lat=25.0330&lng=121.5654&radius=1000&limit=10
```

**Response**:
```json
{
  "count": 5,
  "stations": [
    {
      "sno": "500101001",
      "sna": "YouBike2.0_捷運市政府站(3號出口)",
      "available_rent_bikes": 10,
      "available_return_bikes": 15,
      "distance": 250.5,
      "latitude": "25.0408",
      "longitude": "121.5674"
    }
  ],
  "query": {
    "lat": 25.0330,
    "lng": 121.5654,
    "radius": 1000
  }
}
```

##### Get Station Info
```http
GET /api/station/{station_id}
```

##### Get Stations by Area
```http
GET /api/station/area/中正區
```

##### Get Available Stations
```http
GET /api/station/available?min_bikes=3
```

#### 4. Weather (`/api/weather`)

##### Get Current Weather & AQI
```http
GET /api/weather?location=臺北市&include_aqi=true
```

**Response**:
```json
{
  "location": "臺北市",
  "weather": {
    "locationName": "臺北市",
    "weatherElement": [...]
  },
  "aqi": {
    "sitename": "中山",
    "aqi": "45",
    "status": "良好",
    "pm2.5": "12",
    "county": "臺北市"
  },
  "timestamp": null
}
```

##### Get Weather Forecast
```http
GET /api/weather/forecast?location=臺北市
```

##### Get AQI Data
```http
GET /api/aqi?location=臺北市&limit=5
```

##### Get AQI Status Summary
```http
GET /api/aqi/status
```

#### 5. Statistics (`/api/stats`)

##### Get User Stats
```http
GET /api/stats?user_id=user001
```

**Response**:
```json
{
  "total_rides": 12,
  "total_distance_km": 124.7,
  "total_carbon_saved_kg": 8.3,
  "total_calories": 2450.5,
  "total_duration_hours": 15.3,
  "avg_speed_kmh": 13.5,
  "avg_distance_km": 10.4
}
```

##### Get Leaderboard
```http
GET /api/stats/leaderboard?metric=distance&limit=10
```

##### Get Weekly Stats
```http
GET /api/stats/weekly?user_id=user001
```

##### Get Achievements
```http
GET /api/stats/achievements?user_id=user001
```

## 🏗️ Project Structure

```
backend/
├── app.py                      # Main Flask application
├── data_store.py              # In-memory data storage
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
│
├── routes/                    # Route modules (Blueprints)
│   ├── ride_routes.py        # Ride management endpoints
│   ├── history_routes.py     # History tracking endpoints
│   ├── station_routes.py     # Station information endpoints
│   ├── weather_routes.py     # Weather & AQI endpoints
│   └── stats_routes.py       # Statistics endpoints
│
├── fetch_weather_data.py     # Weather data fetcher
├── fetch_aqi_data.py         # AQI data fetcher
├── fetch_youbike_data.py     # YouBike data fetcher
│
└── data/                      # Data storage directory
    ├── weather_data.json
    ├── aqi_data.json
    └── youbike_data.json
```

## 🧪 Testing the API

### Using curl

**Start a ride**:
```bash
curl -X POST http://127.0.0.1:5000/api/ride/start \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user001"}'
```

**Get nearby stations**:
```bash
curl "http://127.0.0.1:5000/api/station/nearby?lat=25.0330&lng=121.5654&radius=1000&limit=5"
```

**Get weather**:
```bash
curl "http://127.0.0.1:5000/api/weather?location=臺北市"
```

**Get stats**:
```bash
curl "http://127.0.0.1:5000/api/stats?user_id=user001"
```

### Using Python requests

```python
import requests

# Start a ride
response = requests.post('http://127.0.0.1:5000/api/ride/start', json={
    'user_id': 'user001'
})
ride_data = response.json()
print(ride_data)

# Get nearby stations
response = requests.get('http://127.0.0.1:5000/api/station/nearby', params={
    'lat': 25.0330,
    'lng': 121.5654,
    'radius': 1000,
    'limit': 5
})
stations = response.json()
print(stations)
```

## 📊 Data Models

### Ride Record
```python
{
    "ride_id": str,               # UUID
    "user_id": str,               # User identifier
    "start_time": datetime,       # ISO format
    "end_time": datetime,         # ISO format
    "start_location": dict,       # {lat, lng}
    "end_location": dict,         # {lat, lng}
    "paused_time": float,         # seconds
    "duration": float,            # active riding time (seconds)
    "total_duration": float,      # total time including pauses (seconds)
    "distance": float,            # meters
    "avg_speed": float,           # km/h
    "max_speed": float,           # km/h
    "calories": float,            # kcal
    "elevation_profile": list,    # [float] elevation points
    "carbon_reduction": float,    # kg CO2 saved
    "status": str                 # "active", "paused", "completed"
}
```

## 🔧 Configuration

### Environment Variables

Create or modify `.env` file:

```bash
# API Keys
CWA_API_KEY=your_weather_api_key
MOENV_API_KEY=your_aqi_api_key
```

### Flask Configuration

In `app.py`:
- `JSON_AS_ASCII = False` - Support Chinese characters
- `JSON_SORT_KEYS = False` - Maintain key order
- CORS enabled for all `/api/*` endpoints

## 🐛 Troubleshooting

### SSL Certificate Errors

If you encounter SSL errors when fetching external data:

**On macOS**:
```bash
/Applications/Python*/Install\ Certificates.command
```

Or run with SSL verification disabled (development only):
```python
fetcher.fetch_data(verify_ssl=False)
```

### Port Already in Use

Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Module Import Errors

Ensure you're in the correct directory and dependencies are installed:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## 📝 Development Notes

### In-Memory Storage

The current implementation uses in-memory storage (Python dictionaries). Data will be lost when the server restarts. For production:

- Consider using a database (SQLite, PostgreSQL, MongoDB)
- Implement data persistence
- Add user authentication

### Carbon Calculation

Carbon reduction is calculated as:
```python
carbon_kg = distance_km * 0.12  # Assumes 120g CO2 per km for cars
```

### Thread Safety

The `DataStore` class uses threading locks to ensure thread-safe operations in a multi-threaded Flask environment.

## 🚀 Next Steps

1. **Add Database**: Replace in-memory storage with SQLite/PostgreSQL
2. **User Authentication**: Implement JWT or session-based auth
3. **Data Validation**: Add more robust input validation
4. **Rate Limiting**: Add API rate limiting
5. **Logging**: Implement proper logging
6. **Testing**: Add unit and integration tests
7. **Documentation**: Add Swagger/OpenAPI documentation

## 📄 License

This project is part of the TownPass cycling application.

## 👥 Support

For issues or questions, please contact the development team.
