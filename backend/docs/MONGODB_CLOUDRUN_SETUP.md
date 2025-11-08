# MongoDB + Cloud Run Setup Guide

## 🎯 Architecture

```
Frontend (Vue.js)
     ↓
Flask Backend (Cloud Run)
     ↓
MongoDB Atlas (Cloud Database)
```

---

## 📦 Part 1: Local Testing (3 Options)

### **Option A: Local MongoDB (Simplest)**

```bash
# 1. Install MongoDB locally
# macOS:
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# 2. Update .env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=townpass

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run backend
python app.py
```

### **Option B: MongoDB Atlas (Free Cloud - Recommended)**

```bash
# 1. Create MongoDB Atlas account (free)
# Go to: https://www.mongodb.com/cloud/atlas/register

# 2. Create FREE Cluster (M0)
#    - Select cloud provider & region closest to you
#    - Cluster name: townpass-cluster

# 3. Create Database User
#    Database Access → Add New Database User
#    Username: townpass_user
#    Password: <generate strong password>

# 4. Whitelist your IP
#    Network Access → Add IP Address
#    For testing: 0.0.0.0/0 (allow all)
#    For production: Add specific IPs

# 5. Get connection string
#    Clusters → Connect → Connect your application
#    Copy string: mongodb+srv://townpass_user:<password>@cluster.mongodb.net/

# 6. Update .env
MONGODB_URI=mongodb+srv://townpass_user:your_password@cluster0.xxxxx.mongodb.net/
MONGODB_DB_NAME=townpass

# 7. Run backend
python app.py
```

### **Option C: No Database (In-Memory Only)**

```bash
# Just don't set MONGODB_URI
# Ride sessions work, but don't persist

python app.py
```

---

## 🧪 Part 2: Testing the API

### **Install test dependencies**

```bash
pip install requests
```

### **Test MongoDB Connection**

```bash
cd /Users/tedlu/Desktop/townpass-dev/backend
python3 -c "from database import init_database; init_database()"
```

### **Test Ride Persistence**

Create `test_mongodb.py`:

```python
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api/ride"

# 1. Save a ride
ride_data = {
    "user_id": "test_user_123",
    "start_time": "2025-11-08T10:00:00",
    "end_time": "2025-11-08T10:30:00",
    "duration": 1800,  # 30 minutes
    "distance": 5000,  # 5 km
    "calories": 250,
    "avg_speed": 10.0,
    "max_speed": 15.0,
    "route": [
        {"lat": 25.0408, "lng": 121.5674, "timestamp": "2025-11-08T10:00:00"},
        {"lat": 25.0428, "lng": 121.5694, "timestamp": "2025-11-08T10:15:00"}
    ],
    "weather": {"temperature": "22°C", "condition": "Sunny"}
}

print("📝 Saving ride...")
response = requests.post(f"{BASE_URL}/rides", json=ride_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# 2. Get user's rides
print("📚 Getting ride history...")
response = requests.get(f"{BASE_URL}/rides", params={"user_id": "test_user_123"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")

# 3. Get user stats
print("📊 Getting user stats...")
response = requests.get(f"{BASE_URL}/stats", params={"user_id": "test_user_123"})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
```

Run test:
```bash
python test_mongodb.py
```

---

## 🚀 Part 3: Deploy to Cloud Run

### **Prerequisites**

```bash
# 1. Install Google Cloud CLI
# macOS:
brew install google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install

# 2. Login to Google Cloud
gcloud auth login

# 3. Set project
gcloud config set project YOUR_PROJECT_ID
```

### **Create Dockerfile**

Create `/Users/tedlu/Desktop/townpass-dev/backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run with gunicorn for production
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app
```

### **Update requirements.txt**

Add gunicorn for production:
```bash
echo "gunicorn>=21.2.0" >> requirements.txt
```

### **Deploy to Cloud Run**

```bash
# 1. Navigate to backend directory
cd /Users/tedlu/Desktop/townpass-dev/backend

# 2. Build and deploy
gcloud run deploy townpass-backend \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars MONGODB_URI="your_mongodb_atlas_uri" \
  --set-env-vars MONGODB_DB_NAME="townpass" \
  --set-env-vars CWA_API_KEY="your_cwa_key" \
  --max-instances 10 \
  --memory 512Mi

# 3. You'll get a URL like:
# https://townpass-backend-xxxxx-as.a.run.app
```

### **Alternative: Use .env for secrets**

Create `backend/.env.yaml`:

```yaml
MONGODB_URI: "mongodb+srv://user:pass@cluster.mongodb.net/"
MONGODB_DB_NAME: "townpass"
CWA_API_KEY: "your_key"
```

Deploy with env file:
```bash
gcloud run deploy townpass-backend \
  --source . \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --env-vars-file .env.yaml
```

---

## 🔒 Part 4: Security Best Practices

### **For MongoDB Atlas**

1. **Use IP Whitelist**: Only allow Cloud Run IPs
2. **Strong passwords**: Use generated passwords
3. **Read-only users**: Create separate users for different access levels
4. **Enable encryption**: Atlas encrypts by default

### **For Cloud Run**

```bash
# Use Secret Manager instead of env vars
gcloud secrets create mongodb-uri --data-file=-
# Paste your URI, press Ctrl+D

# Deploy with secret
gcloud run deploy townpass-backend \
  --source . \
  --update-secrets MONGODB_URI=mongodb-uri:latest
```

---

## 📊 Part 5: Monitor Your App

### **Check logs**

```bash
gcloud run logs read townpass-backend --limit 50
```

### **View metrics**

```bash
# Open Cloud Console
gcloud run services describe townpass-backend --region asia-east1
```

---

## 💰 Cost Estimate (Free Tier)

- **MongoDB Atlas**: FREE M0 (512MB storage, 100 connections)
- **Cloud Run**: FREE up to 2M requests/month
- **Total**: $0/month for small apps 🎉

---

## 🎯 Quick Start Commands

```bash
# Local development
cd /Users/tedlu/Desktop/townpass-dev/backend
cp .env.example .env
# Edit .env with your MongoDB URI
pip install -r requirements.txt
python app.py

# Deploy to production
gcloud run deploy townpass-backend --source .
```

---

## 🆘 Troubleshooting

### MongoDB connection failed

```bash
# Check if MongoDB URI is set
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('MONGODB_URI'))"

# Test connection
python3 -c "from pymongo import MongoClient; client = MongoClient('your_uri'); print(client.server_info())"
```

### Cloud Run deployment failed

```bash
# Check build logs
gcloud builds list --limit 5

# View specific build
gcloud builds log BUILD_ID
```

### Can't connect to Cloud Run from frontend

```bash
# Check service status
gcloud run services list

# Get service URL
gcloud run services describe townpass-backend --region asia-east1 --format 'value(status.url)'

# Test endpoint
curl https://your-service-url.run.app/health
```

---

## ✅ Success Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created with password
- [ ] IP whitelist configured (0.0.0.0/0 for testing)
- [ ] Connection string copied and added to .env
- [ ] Local backend connects to MongoDB
- [ ] Test API endpoints work locally
- [ ] Dockerfile created
- [ ] Cloud Run service deployed
- [ ] Environment variables set in Cloud Run
- [ ] Frontend updated to use Cloud Run URL
- [ ] All API endpoints working in production

---

**Need help?** Check MongoDB Atlas docs or Cloud Run docs, or test locally first!
