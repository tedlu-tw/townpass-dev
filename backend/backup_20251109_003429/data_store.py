"""
In-Memory Data Storage
Simulates a database using Python dictionaries
"""

from typing import Dict, List, Optional
from datetime import datetime
import threading


class DataStore:
    """Thread-safe in-memory data storage"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._rides: Dict[str, Dict] = {}
        self._active_sessions: Dict[str, Dict] = {}
    
    # Ride operations
    def create_ride(self, ride_id: str, ride_data: Dict) -> None:
        """Create a new ride record"""
        with self._lock:
            self._rides[ride_id] = ride_data
    
    def get_ride(self, ride_id: str) -> Optional[Dict]:
        """Get a specific ride record"""
        with self._lock:
            return self._rides.get(ride_id)
    
    def get_all_rides(self, user_id: str = None) -> List[Dict]:
        """Get all rides, optionally filtered by user_id"""
        with self._lock:
            if user_id:
                return [ride for ride in self._rides.values() if ride.get('user_id') == user_id]
            return list(self._rides.values())
    
    def update_ride(self, ride_id: str, updates: Dict) -> bool:
        """Update a ride record"""
        with self._lock:
            if ride_id in self._rides:
                self._rides[ride_id].update(updates)
                return True
            return False
    
    def delete_ride(self, ride_id: str) -> bool:
        """Delete a ride record"""
        with self._lock:
            if ride_id in self._rides:
                del self._rides[ride_id]
                return True
            return False
    
    # Active session operations
    def create_session(self, ride_id: str, session_data: Dict) -> None:
        """Create a new active session"""
        with self._lock:
            self._active_sessions[ride_id] = session_data
    
    def get_session(self, ride_id: str) -> Optional[Dict]:
        """Get an active session"""
        with self._lock:
            return self._active_sessions.get(ride_id)
    
    def update_session(self, ride_id: str, updates: Dict) -> bool:
        """Update an active session"""
        with self._lock:
            if ride_id in self._active_sessions:
                self._active_sessions[ride_id].update(updates)
                return True
            return False
    
    def delete_session(self, ride_id: str) -> bool:
        """Delete an active session"""
        with self._lock:
            if ride_id in self._active_sessions:
                del self._active_sessions[ride_id]
                return True
            return False
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all active sessions"""
        with self._lock:
            return list(self._active_sessions.values())
    
    # Statistics operations
    def get_user_stats(self, user_id: str = None) -> Dict:
        """Calculate user statistics"""
        with self._lock:
            rides = [ride for ride in self._rides.values() if ride.get('user_id') == user_id] if user_id else list(self._rides.values())
            
            total_rides = len(rides)
            total_distance = sum(ride.get('distance', 0) for ride in rides)
            total_carbon_saved = sum(ride.get('carbon_reduction', 0) for ride in rides)
            total_calories = sum(ride.get('calories', 0) for ride in rides)
            total_duration = sum(ride.get('duration', 0) for ride in rides)
            
            return {
                "total_rides": total_rides,
                "total_distance_km": round(total_distance / 1000, 2),
                "total_carbon_saved_kg": round(total_carbon_saved, 2),
                "total_calories": round(total_calories, 2),
                "total_duration_hours": round(total_duration / 3600, 2)
            }


# Global data store instance
data_store = DataStore()
