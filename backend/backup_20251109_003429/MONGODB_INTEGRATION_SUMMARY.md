# ✅ MongoDB + Cloud Run Integration Complete!

## 🎉 What's Been Done

Your TownPass backend now supports **MongoDB Atlas** for persistent ride data storage while being deployable on **Firebase Cloud Run**!

---

## 📦 New Files Created

1. **`database.py`** - MongoDB connection and operations
   - User profile management
   - Ride CRUD operations
   - Statistics aggregation

2. **`MONGODB_CLOUDRUN_SETUP.md`** - Complete setup guide
   - Local testing with MongoDB
   - MongoDB Atlas setup
   - Cloud Run deployment
   - Security best practices

3. **`test_mongodb.py`** - Test script for MongoDB integration
   - Tests all ride endpoints
   - Validates data persistence
   - Checks stats accumulation

---

## 🔧 Modified Files

1. **`routes/ride_routes.py`** - Added MongoDB endpoints
   - `POST /api/ride/rides` - Save completed ride
   - `GET /api/ride/rides` - Get ride history
   - `GET /api/ride/rides/<id>` - Get specific ride
   - `DELETE /api/ride/rides/<id>` - Delete ride
   - `GET /api/ride/stats` - Get user statistics

2. **`app.py`** - Initialize MongoDB on startup
   - Auto-connects to MongoDB if URI is set
   - Gracefully handles no database scenario
   - Cleans up connection on shutdown

3. **`requirements.txt`** - Added pymongo
   ```
   pymongo>=4.6.0
   ```

4. **`.env.example`** - Added MongoDB config
   ```bash
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=townpass
   ```

---

## 🚀 Quick Start Guide

### **Option 1: Test Locally (No Cloud)**

```bash
# 1. Install local MongoDB
brew install mongodb-community
brew services start mongodb-community

# 2. Update .env
cp .env.example .env
# Edit .env: MONGODB_URI=mongodb://localhost:27017

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start backend
python app.py

# 5. Test MongoDB integration
python test_mongodb.py
```

### **Option 2: Use MongoDB Atlas (Free Cloud)**

```bash
# 1. Create account: https://www.mongodb.com/cloud/atlas/register
# 2. Create FREE M0 cluster
# 3. Get connection string
# 4. Update .env
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/

# 5. Start backend
python app.py

# 6. Test
python test_mongodb.py
```

### **Option 3: No Database (In-Memory Only)**

```bash
# Just run without MONGODB_URI set
python app.py

# Ride sessions work, but don't persist
# Perfect for initial frontend testing
```

---

## 📡 API Endpoints

### **New MongoDB Endpoints**

All under `/api/ride/` prefix:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rides` | Save completed ride |
| GET | `/rides?user_id=xxx` | Get user's ride history |
| GET | `/rides/<ride_id>?user_id=xxx` | Get specific ride |
| DELETE | `/rides/<ride_id>?user_id=xxx` | Delete a ride |
| GET | `/stats?user_id=xxx` | Get user statistics |

### **Example: Save a Ride**

```bash
curl -X POST http://localhost:5000/api/ride/rides \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "duration": 1800,
    "distance": 5000,
    "calories": 250,
    "avg_speed": 10.0,
    "route": [{"lat": 25.04, "lng": 121.56}],
    "weather": {"temperature": "22°C"}
  }'
```

### **Example: Get Ride History**

```bash
curl "http://localhost:5000/api/ride/rides?user_id=user123"
```

### **Example: Get User Stats**

```bash
curl "http://localhost:5000/api/ride/stats?user_id=user123"
```

---

## 🗄️ Database Schema

### **Users Collection**

```json
{
  "user_id": "unique_device_id",
  "created_at": "2025-11-08T10:00:00",
  "total_rides": 10,
  "total_distance": 50000,
  "total_duration": 18000,
  "total_calories": 2500,
  "preferences": {
    "units": "metric",
    "theme": "light"
  }
}
```

### **Rides Collection**

```json
{
  "_id": "ObjectId(...)",
  "user_id": "unique_device_id",
  "start_time": "2025-11-08T10:00:00",
  "end_time": "2025-11-08T10:30:00",
  "duration": 1800,
  "distance": 5000,
  "calories": 250,
  "avg_speed": 10.0,
  "max_speed": 15.0,
  "route": [{"lat": 25.04, "lng": 121.56, "timestamp": "..."}],
  "start_station": {"name": "...", "sno": "..."},
  "end_location": {"lat": 25.05, "lng": 121.57},
  "weather": {"temperature": "22°C", "condition": "Sunny"},
  "created_at": "2025-11-08T10:30:00"
}
```

---

## 🔐 Frontend Integration

### **Generate User ID (localStorage)**

```javascript
// composables/useUserData.js
import { ref } from 'vue'
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

### **Save Ride from Frontend**

```javascript
// composables/useRideStorage.js
import { useUserData } from './useUserData'

export function useRideStorage() {
  const { userId } = useUserData()
  const API_URL = 'http://localhost:5000/api/ride'
  
  const saveRide = async (rideData) => {
    const response = await fetch(`${API_URL}/rides`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        ...rideData
      })
    })
    return await response.json()
  }
  
  const getRideHistory = async () => {
    const response = await fetch(`${API_URL}/rides?user_id=${userId}`)
    return await response.json()
  }
  
  const getUserStats = async () => {
    const response = await fetch(`${API_URL}/stats?user_id=${userId}`)
    return await response.json()
  }
  
  return { saveRide, getRideHistory, getUserStats }
}
```

---

## 🚀 Deploy to Cloud Run

```bash
# 1. Navigate to backend
cd /Users/tedlu/Desktop/townpass-dev/backend

# 2. Create Dockerfile (if not exists)
cat > Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 app:app
EOF

# 3. Add gunicorn to requirements
echo "gunicorn>=21.2.0" >> requirements.txt

# 4. Deploy
gcloud run deploy townpass-backend \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars MONGODB_URI="your_atlas_uri" \
  --set-env-vars MONGODB_DB_NAME="townpass" \
  --set-env-vars CWA_API_KEY="your_key" \
  --memory 512Mi
```

---

## 💰 Costs (Free Tier)

- **MongoDB Atlas M0**: FREE (512MB storage)
- **Cloud Run**: FREE up to 2M requests/month
- **Total**: $0/month for hobby projects! 🎉

---

## ✅ Testing Checklist

- [ ] MongoDB connection works locally
- [ ] Can save rides
- [ ] Can retrieve ride history
- [ ] User stats accumulate correctly
- [ ] Can delete rides
- [ ] Backend works without MongoDB (graceful degradation)
- [ ] MongoDB Atlas connection works
- [ ] Cloud Run deployment successful
- [ ] Frontend can save/retrieve rides

---

## 🆘 Troubleshooting

### Backend won't start

```bash
# Check if MongoDB is running
brew services list | grep mongodb

# Or check connection
python3 -c "from database import init_database; init_database()"
```

### Can't connect to MongoDB Atlas

1. Check IP whitelist (use 0.0.0.0/0 for testing)
2. Verify username/password
3. Test connection string:
```bash
python3 -c "from pymongo import MongoClient; client = MongoClient('your_uri'); print(client.server_info())"
```

### Cloud Run deployment fails

```bash
# Check build logs
gcloud builds list --limit 5

# View errors
gcloud run services describe townpass-backend --region asia-east1
```

---

## 📚 Next Steps

1. ✅ Test locally with MongoDB
2. ✅ Create MongoDB Atlas account
3. ✅ Deploy to Cloud Run
4. 🔨 Update frontend to use new endpoints
5. 🎨 Build ride history UI
6. 📊 Create stats dashboard

---

## 🎯 Key Benefits

✅ **Works with or without database** - Graceful degradation  
✅ **Free to test** - MongoDB Atlas + Cloud Run free tiers  
✅ **Scalable** - MongoDB Atlas handles growth automatically  
✅ **Cloud Run compatible** - Containerized deployment  
✅ **No auth complexity** - Device ID based  
✅ **Easy local testing** - Use local MongoDB or Atlas  

---

**You're all set!** 🚴‍♂️

Test locally first, then deploy to Cloud Run when ready!
