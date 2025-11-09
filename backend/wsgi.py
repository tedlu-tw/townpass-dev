#!/usr/bin/env python3
"""
Production startup script for gunicorn
Initializes MongoDB connection before starting
"""

import os
import sys
from app import app
from database import init_database, db

# Initialize MongoDB connection IMMEDIATELY when module is imported
# This ensures connection is established before any requests
print("=" * 60, flush=True)
print("🚴 TownPass Backend (Production)", flush=True)
print("=" * 60, flush=True)

mongodb_uri = os.getenv('MONGODB_URI')
if mongodb_uri:
    print("🔧 Connecting to MongoDB...", flush=True)
    try:
        if init_database():
            print("✅ MongoDB connected successfully", flush=True)
        else:
            print("❌ MongoDB connection failed", flush=True)
            sys.stderr.write("ERROR: MongoDB connection failed\n")
    except Exception as e:
        print(f"❌ MongoDB error: {e}", flush=True)
        sys.stderr.write(f"ERROR: MongoDB initialization error: {e}\n")
else:
    print("⚠️  No MONGODB_URI environment variable", flush=True)
    sys.stderr.write("WARNING: No MONGODB_URI set\n")

print("=" * 60, flush=True)
print(f"Database connected: {db.is_connected()}", flush=True)
print("=" * 60, flush=True)

# Export app for gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
