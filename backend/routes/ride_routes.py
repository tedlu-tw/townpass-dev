"""
Ride Routes - Handle ride session and data operations
All operations now use MongoDB for persistence

Active Sessions:
POST /start - Start a new ride session
POST /update - Update ride metrics
POST /finish - Finish a ride session
POST /pause - Pause a ride session
POST /resume - Resume a paused ride session
GET /active - Get active ride sessions

Completed Rides:
POST /rides - Save a completed ride
GET /rides - Get user's ride history
GET /rides/<ride_id> - Get specific ride details
DELETE /rides/<ride_id> - Delete a ride
GET /stats - Get user statistics
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
from database import get_db

ride_bp = Blueprint('ride', __name__)


def validate_required_fields(data: dict, required_fields: list) -> tuple:
    """
    Validate that all required fields are present in the request data
    
    Returns:
        (is_valid: bool, error_message: str)
    """
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, ""


@ride_bp.route('/start', methods=['POST'])
def start_ride():
    """
    Start a new ride session
    
    Request body:
    {
        "user_id": str (required),
        "start_location": {"lat": float, "lng": float} (required - GPS coordinates where ride starts)
    }
    
    Response:
    {
        "ride_id": str,
        "user_id": str,
        "start_time": str,
        "message": str
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['user_id', 'start_location'])
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Generate ride ID
        ride_id = str(uuid.uuid4())
        user_id = data['user_id']
        start_time = datetime.now()
        
        # Create session data
        session_data = {
            "ride_id": ride_id,
            "user_id": user_id,
            "start_time": start_time.isoformat(),
            "start_location": data.get('start_location'),  # {lat, lng} GPS coordinates
            "paused_time": 0.0,
            "distance": 0.0,
            "avg_speed": 0.0,
            "max_speed": 0.0,
            "calories": 0.0,
            "route": [],  # Will accumulate GPS points during ride
            "elevation_profile": [],
            "status": "active"
        }
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({"error": "Database not available"}), 503
        
        # Ensure user exists
        db.get_or_create_user(user_id)
        
        # Store in active sessions
        if not db.create_session(ride_id, session_data):
            return jsonify({"error": "Failed to create session"}), 500
        
        return jsonify({
            "ride_id": ride_id,
            "user_id": user_id,
            "start_time": start_time.isoformat(),
            "message": "Ride session started."
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Failed to start ride: {str(e)}"}), 500


@ride_bp.route('/update', methods=['POST'])
def update_ride():
    """
    Update ride metrics during active ride
    
    Request body:
    {
        "ride_id": str (required),
        "distance": float (optional, total distance in meters),
        "speed": float (optional, current speed in km/h),
        "calories": float (optional, total calories burned),
        "paused_time": float (optional, total paused time in seconds),
        "elevation": float (optional, current elevation in meters),
        "current_location": {"lat": float, "lng": float} (optional - adds GPS point to route)
    }
    
    Response:
    {
        "ride_id": str,
        "message": str,
        "updated_fields": dict
    }
    
    Note: Providing current_location will automatically add a GPS point to the route array
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['ride_id'])
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        ride_id = data['ride_id']
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({"error": "Database not available"}), 503
        
        # Check if session exists
        session = db.get_session(ride_id)
        if not session:
            return jsonify({"error": "Ride session not found or already finished"}), 404
        
        # Prepare updates
        updates = {}
        updated_fields = {}
        
        # Update distance
        if 'distance' in data:
            updates['distance'] = float(data['distance'])
            updated_fields['distance'] = updates['distance']
        
        # Update speed and calculate average
        if 'speed' in data:
            current_speed = float(data['speed'])
            updates['max_speed'] = max(session.get('max_speed', 0), current_speed)
            updated_fields['current_speed'] = current_speed
            updated_fields['max_speed'] = updates['max_speed']
        
        # Update calories
        if 'calories' in data:
            updates['calories'] = float(data['calories'])
            updated_fields['calories'] = updates['calories']
        
        # Update paused time
        if 'paused_time' in data:
            updates['paused_time'] = float(data['paused_time'])
            updated_fields['paused_time'] = updates['paused_time']
        
        # Update elevation profile
        if 'elevation' in data:
            elevation_profile = session.get('elevation_profile', [])
            elevation_profile.append(float(data['elevation']))
            updates['elevation_profile'] = elevation_profile
            updated_fields['elevation_added'] = True
        
        # Update current location and add to route
        if 'current_location' in data:
            location = data['current_location']
            updates['current_location'] = location
            updated_fields['current_location'] = location
            
            # Add GPS point to route history
            route = session.get('route', [])
            route_point = {
                'lat': location.get('lat'),
                'lng': location.get('lng'),
                'timestamp': datetime.now().isoformat()
            }
            route.append(route_point)
            updates['route'] = route
            updated_fields['route_point_added'] = True
        
        # Apply updates
        if not db.update_session(ride_id, updates):
            return jsonify({"error": "Failed to update session"}), 500
        
        return jsonify({
            "ride_id": ride_id,
            "message": "Ride metrics updated successfully.",
            "updated_fields": updated_fields
        }), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid data type: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to update ride: {str(e)}"}), 500


@ride_bp.route('/finish', methods=['POST'])
def finish_ride():
    """
    Finish a ride session and save to MongoDB
    
    Request body:
    {
        "ride_id": str (required),
        "end_location": {"lat": float, "lng": float} (required - GPS coordinates),
        "weather": {"temperature": str, "condition": str, "aqi": str} (optional)
    }
    
    Response:
    {
        "ride_id": str,
        "message": str,
        "summary": {
            "duration_minutes": float,
            "distance_km": float,
            "avg_speed_kmh": float,
            "max_speed_kmh": float,
            "calories": float,
            "carbon_saved_kg": float
        }
    }
    
    Saved to MongoDB with schema:
    {
        "user_id": str,
        "start_time": str (ISO),
        "end_time": str (ISO),
        "duration": int (seconds),
        "distance": int (meters),
        "calories": int,
        "avg_speed": float (km/h),
        "max_speed": float (km/h),
        "route": [{lat, lng, timestamp}, ...],
        "start_location": {lat, lng} (GPS coordinates where ride started),
        "end_location": {lat, lng} (GPS coordinates where ride ended),
        "weather": {},
        "created_at": datetime
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        # Validate required fields
        is_valid, error_msg = validate_required_fields(data, ['ride_id'])
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        ride_id = data['ride_id']
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({"error": "Database not available"}), 503
        
        # Get active session
        session = db.get_session(ride_id)
        if not session:
            return jsonify({"error": "Ride session not found or already finished"}), 404
        
        # Calculate final metrics
        end_time = datetime.now()
        start_time = datetime.fromisoformat(session['start_time'])
        total_duration = (end_time - start_time).total_seconds()
        active_duration = total_duration - session.get('paused_time', 0)
        
        distance_km = session.get('distance', 0) / 1000
        
        # Calculate average speed (distance in km / time in hours)
        avg_speed = (distance_km / (active_duration / 3600)) if active_duration > 0 else 0
        
        # Calculate carbon reduction (assuming 120g CO2 per km for cars)
        carbon_reduction = distance_km * 0.12  # kg
        
        # Create final ride record matching preferred schema
        ride_record = {
            "start_time": session['start_time'],
            "end_time": end_time.isoformat(),
            "duration": int(active_duration),  # seconds as int
            "distance": int(session.get('distance', 0)),  # meters as int
            "calories": int(session.get('calories', 0)),  # as int
            "avg_speed": round(avg_speed, 2),  # km/h as float
            "max_speed": float(session.get('max_speed', 0)),  # km/h as float
            "route": session.get('route', []),  # array of {lat, lng, timestamp}
            "start_location": session.get('start_location'),  # {lat, lng} GPS coordinates where ride started
            "end_location": data.get('end_location'),  # {lat, lng} GPS coordinates where ride ended
            "weather": data.get('weather', {})  # weather at ride completion
        }
        
        # Save to rides history
        saved_ride_id = db.save_ride(session['user_id'], ride_record)
        if not saved_ride_id:
            return jsonify({"error": "Failed to save ride"}), 500
        
        # Remove from active sessions
        db.delete_session(ride_id)
        
        # Prepare summary
        summary = {
            "duration_minutes": round(active_duration / 60, 1),
            "distance_km": round(distance_km, 2),
            "avg_speed_kmh": round(avg_speed, 2),
            "max_speed_kmh": round(session.get('max_speed', 0), 2),
            "calories": round(session.get('calories', 0), 2),
            "carbon_saved_kg": round(carbon_reduction, 3)
        }
        
        return jsonify({
            "ride_id": ride_id,
            "message": "Ride session finished successfully.",
            "summary": summary
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to finish ride: {str(e)}"}), 500


@ride_bp.route('/active', methods=['GET'])
def get_active_rides():
    """
    Get all active ride sessions
    
    Response:
    {
        "count": int,
        "sessions": list
    }
    """
    try:
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({"error": "Database not available"}), 503
        
        # Get all sessions or filter by user
        user_id = request.args.get('user_id')
        sessions = db.get_all_sessions(user_id=user_id)
        
        return jsonify({
            "count": len(sessions),
            "sessions": sessions
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get active rides: {str(e)}"}), 500


@ride_bp.route('/pause', methods=['POST'])
def pause_ride():
    """
    Pause a ride session (optional endpoint for future use)
    
    Request body:
    {
        "ride_id": str
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        ride_id = data.get('ride_id')
        if not ride_id:
            return jsonify({"error": "ride_id is required"}), 400
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({"error": "Database not available"}), 503
        
        session = db.get_session(ride_id)
        if not session:
            return jsonify({"error": "Ride session not found"}), 404
        
        # Update session status
        db.update_session(ride_id, {"status": "paused"})
        
        return jsonify({
            "ride_id": ride_id,
            "message": "Ride session paused."
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to pause ride: {str(e)}"}), 500


@ride_bp.route('/resume', methods=['POST'])
def resume_ride():
    """
    Resume a paused ride session (optional endpoint for future use)
    
    Request body:
    {
        "ride_id": str
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        ride_id = data.get('ride_id')
        if not ride_id:
            return jsonify({"error": "ride_id is required"}), 400
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({"error": "Database not available"}), 503
        
        session = db.get_session(ride_id)
        if not session:
            return jsonify({"error": "Ride session not found"}), 404
        
        # Update session status
        db.update_session(ride_id, {"status": "active"})
        
        return jsonify({
            "ride_id": ride_id,
            "message": "Ride session resumed."
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to resume ride: {str(e)}"}), 500


# ==================== MongoDB Persistence Endpoints ====================

@ride_bp.route('/rides', methods=['POST'])
def save_ride():
    """
    Save a completed ride to MongoDB (manual save, not from active session)
    
    Request body (matching preferred schema):
    {
        "user_id": str (required),
        "start_time": str (ISO format),
        "end_time": str (ISO format),
        "duration": int (seconds),
        "distance": int (meters),
        "calories": int,
        "avg_speed": float (km/h),
        "max_speed": float (km/h),
        "route": [{lat, lng, timestamp}, ...],
        "start_location": {lat, lng} (required - GPS coordinates where ride started),
        "end_location": {lat, lng} (required - GPS coordinates where ride ended),
        "weather": {temperature, condition, aqi} (optional)
    }
    
    Response:
    {
        "success": bool,
        "ride_id": str,
        "message": str
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field: user_id"
            }), 400
        
        user_id = data['user_id']
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({
                "success": False,
                "error": "Database not available"
            }), 503
        
        # Ensure user exists
        db.get_or_create_user(user_id)
        
        # Save ride
        ride_id = db.save_ride(user_id, data)
        
        if ride_id:
            return jsonify({
                "success": True,
                "ride_id": ride_id,
                "message": "Ride saved successfully"
            }), 201
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save ride"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to save ride: {str(e)}"
        }), 500


@ride_bp.route('/rides', methods=['GET'])
def get_rides():
    """
    Get user's ride history from MongoDB
    
    Query parameters:
    - user_id: User identifier (required)
    - limit: Maximum number of rides (default: 50)
    - skip: Number of rides to skip (default: 0)
    
    Response:
    {
        "count": int,
        "rides": list,
        "user_id": str
    }
    """
    try:
        user_id = request.args.get('user_id')
        limit = request.args.get('limit', type=int, default=50)
        skip = request.args.get('skip', type=int, default=0)
        
        if not user_id:
            return jsonify({
                "error": "Missing required parameter: user_id"
            }), 400
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({
                "error": "Database not available"
            }), 503
        
        # Get rides
        rides = db.get_user_rides(user_id, limit=limit, skip=skip)
        
        return jsonify({
            "count": len(rides),
            "rides": rides,
            "user_id": user_id
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get rides: {str(e)}"
        }), 500


@ride_bp.route('/rides/<ride_id>', methods=['GET'])
def get_ride_detail(ride_id):
    """
    Get specific ride details from MongoDB
    
    Query parameters:
    - user_id: User identifier (for authorization)
    
    Response:
    {
        "ride": dict
    }
    """
    try:
        user_id = request.args.get('user_id')
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({
                "error": "Database not available"
            }), 503
        
        # Get ride
        ride = db.get_ride_by_id(ride_id, user_id=user_id)
        
        if not ride:
            return jsonify({
                "error": "Ride not found"
            }), 404
        
        return jsonify({
            "ride": ride
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get ride: {str(e)}"
        }), 500


@ride_bp.route('/rides/<ride_id>', methods=['DELETE'])
def delete_ride_record(ride_id):
    """
    Delete a ride from MongoDB
    
    Query parameters:
    - user_id: User identifier (required, for authorization)
    
    Response:
    {
        "success": bool,
        "message": str
    }
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                "success": False,
                "error": "Missing required parameter: user_id"
            }), 400
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({
                "success": False,
                "error": "Database not available"
            }), 503
        
        # Delete ride
        success = db.delete_ride(ride_id, user_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Ride deleted successfully"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Ride not found or unauthorized"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to delete ride: {str(e)}"
        }), 500


@ride_bp.route('/stats', methods=['GET'])
def get_user_stats():
    """
    Get user statistics from MongoDB
    
    Query parameters:
    - user_id: User identifier (required)
    
    Response:
    {
        "user_id": str,
        "stats": {
            "total_rides": int,
            "total_distance": float,
            "total_duration": int,
            "total_calories": int,
            "avg_distance": float,
            "avg_duration": float
        }
    }
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                "error": "Missing required parameter: user_id"
            }), 400
        
        # Get database
        db = get_db()
        if not db.is_connected():
            return jsonify({
                "error": "Database not available"
            }), 503
        
        # Ensure user exists
        db.get_or_create_user(user_id)
        
        # Get stats
        stats = db.get_user_stats(user_id)
        
        return jsonify({
            "user_id": user_id,
            "stats": stats
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get stats: {str(e)}"
        }), 500
