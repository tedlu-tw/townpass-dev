#!/usr/bin/env python3
"""
TownPass Backend - Flask API Server
Main application entry point with Blueprint registration
"""

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import blueprints
from routes.ride_routes import ride_bp
from routes.station_routes import station_bp
from routes.weather_routes import weather_bp

# Import database
from database import init_database, db

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure app
app.config['JSON_AS_ASCII'] = False  # Support Chinese characters in JSON
app.config['JSON_SORT_KEYS'] = False  # Maintain key order

# Register blueprints
app.register_blueprint(ride_bp, url_prefix='/api/ride')
app.register_blueprint(station_bp, url_prefix='/api/station')
app.register_blueprint(weather_bp, url_prefix='/api')


# Root endpoint
@app.route('/')
def index():
    """Root endpoint - API information"""
    return jsonify({
        "name": "TownPass Backend API",
        "version": "1.0.0",
        "status": "running",
        "database": "MongoDB Atlas",
        "endpoints": {
            "ride_session": {
                "POST /api/ride/start": "Start a new ride session",
                "POST /api/ride/update": "Update ride metrics",
                "POST /api/ride/finish": "Finish a ride session",
                "POST /api/ride/pause": "Pause a ride session",
                "POST /api/ride/resume": "Resume a ride session",
                "GET /api/ride/active": "Get active ride sessions"
            },
            "ride_history": {
                "POST /api/ride/rides": "Save a completed ride",
                "GET /api/ride/rides": "Get all ride history",
                "GET /api/ride/rides/<ride_id>": "Get specific ride details",
                "DELETE /api/ride/rides/<ride_id>": "Delete a ride record"
            },
            "stats": {
                "GET /api/ride/stats": "Get user statistics"
            },
            "station": {
                "GET /api/station/nearby": "Get nearby YouBike stations",
                "GET /api/station/<station_id>": "Get specific station info",
                "GET /api/station/area/<area>": "Get stations by area",
                "GET /api/station/available": "Get stations with available bikes"
            },
            "weather": {
                "GET /api/weather": "Get current weather and AQI data"
            }
        },
        "documentation": "/docs"
    })


# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "TownPass Backend is running"
    }), 200


# Global error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request"""
    return jsonify({
        "error": "Bad Request",
        "message": str(error)
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found"""
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource was not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed"""
    return jsonify({
        "error": "Method Not Allowed",
        "message": "The method is not allowed for the requested URL"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error"""
    return jsonify({
        "error": "Internal Server Error",
        "message": "An internal error occurred"
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚴 TownPass Backend API Server")
    print("=" * 60)
    
    # Initialize MongoDB connection
    mongodb_uri = os.getenv('MONGODB_URI')
    if mongodb_uri:
        print("� Initializing MongoDB connection...")
        if init_database():
            print("✅ MongoDB connected successfully")
        else:
            print("⚠️  MongoDB connection failed - ride persistence disabled")
            print("💡 App will still work, but ride history won't be saved")
    else:
        print("⚠️  MONGODB_URI not set - running without database")
        print("💡 Ride sessions will work but won't persist")
    
    print("=" * 60)
    print("�📍 Server running on: http://127.0.0.1:5000")
    print("📖 API Documentation: http://127.0.0.1:5000/")
    print("💚 Health Check: http://127.0.0.1:5000/health")
    print("=" * 60)
    
    # Run the Flask app
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    finally:
        # Close MongoDB connection on shutdown
        if db.is_connected():
            db.disconnect()
