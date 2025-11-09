#!/usr/bin/env python3
"""
Test MongoDB Atlas connection
This script helps diagnose MongoDB connection issues
"""

import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import certifi

# Load environment variables
load_dotenv()

def test_connection():
    """Test MongoDB connection with different configurations"""
    
    uri = os.getenv('MONGODB_URI')
    if not uri:
        print("❌ MONGODB_URI not found in environment variables")
        sys.exit(1)
    
    print("=" * 60)
    print("MongoDB Connection Test")
    print("=" * 60)
    print(f"URI (masked): {uri[:20]}...{uri[-20:]}")
    print()
    
    # Test 1: Basic connection with defaults
    print("Test 1: Basic connection with defaults")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ SUCCESS: Basic connection works!")
        client.close()
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
    print()
    
    # Test 2: Connection with certifi
    print("Test 2: Connection with certifi CA bundle")
    try:
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            tlsCAFile=certifi.where()
        )
        client.admin.command('ping')
        print("✅ SUCCESS: Connection with certifi works!")
        client.close()
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
    print()
    
    # Test 3: Connection with explicit TLS settings
    print("Test 3: Connection with explicit TLS=True")
    try:
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            tls=True
        )
        client.admin.command('ping')
        print("✅ SUCCESS: Connection with TLS=True works!")
        client.close()
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
    print()
    
    # Test 4: Connection with TLS and certifi
    print("Test 4: Connection with TLS=True and certifi")
    try:
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsCAFile=certifi.where()
        )
        client.admin.command('ping')
        print("✅ SUCCESS: Connection with TLS and certifi works!")
        client.close()
    except Exception as e:
        print(f"❌ FAILED: {str(e)[:200]}")
    print()
    
    # Test 5: Print system info
    print("System Information:")
    import ssl
    print(f"  Python SSL version: {ssl.OPENSSL_VERSION}")
    print(f"  Certifi CA bundle: {certifi.where()}")
    print()

if __name__ == "__main__":
    test_connection()
