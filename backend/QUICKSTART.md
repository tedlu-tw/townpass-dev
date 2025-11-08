# 🚀 Quick Start Guide - TownPass Backend

## Step 1: Navigate to Backend Directory

```bash
cd /Users/tedlu/Desktop/townpass-dev/backend
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask Flask-CORS requests python-dotenv
```

## Step 3: Start the Server

### Option A: Using Python directly
```bash
python app.py
```

### Option B: Using the start script
```bash
./start_server.sh
```

## Step 4: Verify Server is Running

Open your browser and visit:
- http://127.0.0.1:5000/ (API documentation)
- http://127.0.0.1:5000/health (Health check)

Or use curl:
```bash
curl http://127.0.0.1:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "TownPass Backend is running"
}
```

## Step 5: Test the API

### Using the test script:
```bash
python test_api.py
```

### Manual testing with curl:

**1. Start a ride:**
```bash
curl -X POST http://127.0.0.1:5000/api/ride/start \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user001"}'
```

**2. Get nearby stations:**
```bash
curl "http://127.0.0.1:5000/api/station/nearby?lat=25.0330&lng=121.5654&radius=1000&limit=5"
```

**3. Get weather:**
```bash
curl "http://127.0.0.1:5000/api/weather?location=臺北市"
```

**4. Get stats:**
```bash
curl "http://127.0.0.1:5000/api/stats?user_id=user001"
```

## 📋 Available Endpoints

### Ride Management
- `POST /api/ride/start` - Start a ride
- `POST /api/ride/update` - Update ride metrics
- `POST /api/ride/finish` - Finish a ride

### History
- `GET /api/history` - Get all rides
- `GET /api/history/<ride_id>` - Get specific ride
- `DELETE /api/history/<ride_id>` - Delete a ride

### Stations
- `GET /api/station/nearby` - Get nearby stations
- `GET /api/station/<station_id>` - Get station info
- `GET /api/station/available` - Get available stations

### Weather
- `GET /api/weather` - Get weather & AQI
- `GET /api/aqi` - Get AQI data

### Statistics
- `GET /api/stats` - Get user statistics
- `GET /api/stats/leaderboard` - Get leaderboard
- `GET /api/stats/achievements` - Get achievements

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "Address already in use"
**Solution:** Kill the process using port 5000
```bash
lsof -ti:5000 | xargs kill -9
```

Or change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### SSL Certificate Errors
**Solution (macOS):**
```bash
/Applications/Python*/Install\ Certificates.command
```

## 📖 Full Documentation

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for complete API documentation.

## 🎯 Next Steps

1. ✅ Start the backend server
2. ✅ Test with `test_api.py`
3. 🔄 Connect your frontend to the API
4. 🚀 Start building!

---

**Need help?** Check the full documentation or the troubleshooting section.
