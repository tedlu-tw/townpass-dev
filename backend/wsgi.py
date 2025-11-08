#!/usr/bin/env python3
"""
Production startup script for gunicorn
Initializes MongoDB connection before starting
"""

import os
from app import app
from database import init_database, db

# Initialize MongoDB
print("=" * 60)
print("🚴 TownPass Backend (Production)")
print("=" * 60)

mongodb_uri = os.getenv('MONGODB_URI')
if mongodb_uri:
    print("🔧 Connecting to MongoDB...")
    if init_database():
        print("✅ MongoDB connected")
    else:
        print("❌ MongoDB failed")
else:
    print("⚠️  No MONGODB_URI")

print("=" * 60)

# Export app for gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
