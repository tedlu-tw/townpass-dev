"""
MongoDB Database Connection
Handles connection to MongoDB Atlas for ride data storage
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
from typing import Optional, Dict, List

# Load environment variables
load_dotenv()

class Database:
    """MongoDB database connection and operations"""
    
    def __init__(self):
        """Initialize MongoDB connection"""
        self.client: Optional[MongoClient] = None
        self.db = None
        self.rides_collection = None
        self.users_collection = None
        self.sessions_collection = None
        
    def connect(self, connection_string: str = None) -> bool:
        """
        Connect to MongoDB
        
        Args:
            connection_string: MongoDB connection string (default: from MONGODB_URI env var)
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Get connection string from env or parameter
            uri = connection_string or os.getenv('MONGODB_URI')
            
            if not uri:
                print("❌ MONGODB_URI not found in environment variables")
                return False
            
            # For local testing, use local MongoDB
            if uri.startswith('mongodb://localhost'):
                print("🔧 Connecting to local MongoDB...")
            else:
                print("☁️  Connecting to MongoDB Atlas...")
            
            # Create client with timeout
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database (create if doesn't exist)
            db_name = os.getenv('MONGODB_DB_NAME', 'townpass')
            self.db = self.client[db_name]
            
            # Get collections
            self.rides_collection = self.db['rides']
            self.users_collection = self.db['users']
            self.sessions_collection = self.db['active_sessions']
            
            print(f"✅ Connected to MongoDB database: {db_name}")
            return True
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")
    
    def is_connected(self) -> bool:
        """Check if connected to MongoDB"""
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
        except:
            pass
        return False
    
    # ==================== User Operations ====================
    
    def get_or_create_user(self, user_id: str) -> Dict:
        """
        Get user profile or create if doesn't exist
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            User profile document
        """
        user = self.users_collection.find_one({'user_id': user_id})
        
        if not user:
            # Create new user profile
            user = {
                'user_id': user_id,
                'created_at': datetime.utcnow(),
                'total_rides': 0,
                'total_distance': 0,  # meters
                'total_duration': 0,  # seconds
                'total_calories': 0,
                'preferences': {
                    'units': 'metric',
                    'theme': 'light'
                }
            }
            self.users_collection.insert_one(user)
            print(f"✅ Created new user: {user_id}")
        
        return user
    
    def update_user_stats(self, user_id: str, ride_data: Dict) -> bool:
        """
        Update user statistics after completing a ride
        
        Args:
            user_id: User identifier
            ride_data: Ride data containing distance, duration, calories
            
        Returns:
            True if successful
        """
        try:
            self.users_collection.update_one(
                {'user_id': user_id},
                {
                    '$inc': {
                        'total_rides': 1,
                        'total_distance': ride_data.get('distance', 0),
                        'total_duration': ride_data.get('duration', 0),
                        'total_calories': ride_data.get('calories', 0)
                    },
                    '$set': {
                        'last_ride_at': datetime.utcnow()
                    }
                }
            )
            return True
        except Exception as e:
            print(f"❌ Failed to update user stats: {e}")
            return False
    
    # ==================== Ride Operations ====================
    
    def save_ride(self, user_id: str, ride_data: Dict) -> Optional[str]:
        """
        Save a completed ride
        
        Args:
            user_id: User identifier
            ride_data: Ride information
            
        Returns:
            Ride ID if successful, None otherwise
        """
        try:
            ride = {
                'user_id': user_id,
                'start_time': ride_data.get('start_time'),
                'end_time': ride_data.get('end_time'),
                'duration': int(ride_data.get('duration', 0)),  # seconds
                'distance': int(ride_data.get('distance', 0)),  # meters
                'calories': int(ride_data.get('calories', 0)),
                'avg_speed': float(ride_data.get('avg_speed', 0.0)),  # km/h
                'max_speed': float(ride_data.get('max_speed', 0.0)),  # km/h
                'route': ride_data.get('route', []),  # array of {lat, lng, timestamp}
                'start_station': ride_data.get('start_station'),  # {name, sno}
                'end_location': ride_data.get('end_location'),  # {lat, lng}
                'weather': ride_data.get('weather', {}),
                'created_at': datetime.utcnow()
            }
            
            result = self.rides_collection.insert_one(ride)
            
            # Update user stats
            self.update_user_stats(user_id, ride_data)
            
            print(f"✅ Saved ride: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"❌ Failed to save ride: {e}")
            return None
    
    def get_user_rides(self, user_id: str, limit: int = 50, skip: int = 0) -> List[Dict]:
        """
        Get rides for a specific user
        
        Args:
            user_id: User identifier
            limit: Maximum number of rides to return
            skip: Number of rides to skip (for pagination)
            
        Returns:
            List of ride documents
        """
        try:
            rides = list(
                self.rides_collection
                .find({'user_id': user_id})
                .sort('created_at', -1)  # Most recent first
                .skip(skip)
                .limit(limit)
            )
            
            # Convert ObjectId to string
            for ride in rides:
                ride['_id'] = str(ride['_id'])
            
            return rides
            
        except Exception as e:
            print(f"❌ Failed to get user rides: {e}")
            return []
    
    def get_ride_by_id(self, ride_id: str, user_id: str = None) -> Optional[Dict]:
        """
        Get a specific ride by ID
        
        Args:
            ride_id: Ride identifier
            user_id: Optional user ID for authorization
            
        Returns:
            Ride document or None
        """
        try:
            from bson.objectid import ObjectId
            
            query = {'_id': ObjectId(ride_id)}
            if user_id:
                query['user_id'] = user_id
            
            ride = self.rides_collection.find_one(query)
            
            if ride:
                ride['_id'] = str(ride['_id'])
            
            return ride
            
        except Exception as e:
            print(f"❌ Failed to get ride: {e}")
            return None
    
    def delete_ride(self, ride_id: str, user_id: str) -> bool:
        """
        Delete a ride
        
        Args:
            ride_id: Ride identifier
            user_id: User identifier (for authorization)
            
        Returns:
            True if successful
        """
        try:
            from bson.objectid import ObjectId
            
            result = self.rides_collection.delete_one({
                '_id': ObjectId(ride_id),
                'user_id': user_id
            })
            
            return result.deleted_count > 0
            
        except Exception as e:
            print(f"❌ Failed to delete ride: {e}")
            return False
    
    def get_user_stats(self, user_id: str) -> Dict:
        """
        Get aggregated statistics for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Statistics dictionary
        """
        try:
            user = self.users_collection.find_one({'user_id': user_id})
            
            if not user:
                return {
                    'total_rides': 0,
                    'total_distance': 0,
                    'total_duration': 0,
                    'total_calories': 0
                }
            
            return {
                'total_rides': user.get('total_rides', 0),
                'total_distance': user.get('total_distance', 0),
                'total_duration': user.get('total_duration', 0),
                'total_calories': user.get('total_calories', 0),
                'avg_distance': user.get('total_distance', 0) / max(user.get('total_rides', 1), 1),
                'avg_duration': user.get('total_duration', 0) / max(user.get('total_rides', 1), 1)
            }
            
        except Exception as e:
            print(f"❌ Failed to get user stats: {e}")
            return {}
    
    # ==================== Active Session Operations ====================
    
    def create_session(self, ride_id: str, session_data: Dict) -> bool:
        """
        Create an active ride session
        
        Args:
            ride_id: Unique ride identifier
            session_data: Session information
            
        Returns:
            True if successful
        """
        try:
            session = {
                'ride_id': ride_id,
                'user_id': session_data.get('user_id'),
                'start_time': session_data.get('start_time'),
                'start_location': session_data.get('start_location'),
                'current_location': session_data.get('current_location'),
                'distance': session_data.get('distance', 0),
                'avg_speed': session_data.get('avg_speed', 0),
                'max_speed': session_data.get('max_speed', 0),
                'calories': session_data.get('calories', 0),
                'paused_time': session_data.get('paused_time', 0),
                'elevation_profile': session_data.get('elevation_profile', []),
                'status': session_data.get('status', 'active'),
                'created_at': datetime.utcnow()
            }
            
            self.sessions_collection.insert_one(session)
            print(f"✅ Created active session: {ride_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create session: {e}")
            return False
    
    def get_session(self, ride_id: str) -> Optional[Dict]:
        """
        Get an active session by ride ID
        
        Args:
            ride_id: Ride identifier
            
        Returns:
            Session document or None
        """
        try:
            session = self.sessions_collection.find_one({'ride_id': ride_id})
            if session:
                session['_id'] = str(session['_id'])
            return session
        except Exception as e:
            print(f"❌ Failed to get session: {e}")
            return None
    
    def update_session(self, ride_id: str, updates: Dict) -> bool:
        """
        Update an active session
        
        Args:
            ride_id: Ride identifier
            updates: Fields to update
            
        Returns:
            True if successful
        """
        try:
            result = self.sessions_collection.update_one(
                {'ride_id': ride_id},
                {'$set': updates}
            )
            return result.modified_count > 0 or result.matched_count > 0
        except Exception as e:
            print(f"❌ Failed to update session: {e}")
            return False
    
    def delete_session(self, ride_id: str) -> bool:
        """
        Delete an active session
        
        Args:
            ride_id: Ride identifier
            
        Returns:
            True if successful
        """
        try:
            result = self.sessions_collection.delete_one({'ride_id': ride_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"❌ Failed to delete session: {e}")
            return False
    
    def get_all_sessions(self, user_id: str = None) -> List[Dict]:
        """
        Get all active sessions, optionally filtered by user
        
        Args:
            user_id: Optional user identifier
            
        Returns:
            List of session documents
        """
        try:
            query = {'user_id': user_id} if user_id else {}
            sessions = list(self.sessions_collection.find(query))
            
            # Convert ObjectId to string
            for session in sessions:
                session['_id'] = str(session['_id'])
            
            return sessions
        except Exception as e:
            print(f"❌ Failed to get sessions: {e}")
            return []
    
    def get_user_active_session(self, user_id: str) -> Optional[Dict]:
        """
        Get user's current active session (if any)
        
        Args:
            user_id: User identifier
            
        Returns:
            Active session or None
        """
        try:
            session = self.sessions_collection.find_one({
                'user_id': user_id,
                'status': 'active'
            })
            if session:
                session['_id'] = str(session['_id'])
            return session
        except Exception as e:
            print(f"❌ Failed to get user active session: {e}")
            return None


# Global database instance
db = Database()


def init_database():
    """Initialize database connection on app startup"""
    return db.connect()


def get_db() -> Database:
    """Get database instance"""
    return db
