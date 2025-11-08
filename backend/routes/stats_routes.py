"""
Stats Routes - Handle user statistics
GET /stats - Get user statistics
"""

from flask import Blueprint, request, jsonify
from database import get_db

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get user statistics
    
    Query parameters:
    - user_id: Filter by user ID (optional, if not provided returns global stats)
    
    Response:
    {
        "total_rides": int,
        "total_distance_km": float,
        "total_carbon_saved_kg": float,
        "total_calories": float,
        "total_duration_hours": float,
        "avg_speed_kmh": float (optional),
        "avg_distance_km": float (optional)
    }
    """
    try:
        user_id = request.args.get('user_id')
        
        # Get stats from data store
        stats = data_store.get_user_stats(user_id)
        
        # Calculate additional metrics
        rides = data_store.get_all_rides(user_id)
        
        if rides:
            # Calculate average speed
            total_distance = sum(ride.get('distance', 0) for ride in rides)
            total_duration = sum(ride.get('duration', 0) for ride in rides)
            
            if total_duration > 0:
                avg_speed = (total_distance / 1000) / (total_duration / 3600)
                stats['avg_speed_kmh'] = round(avg_speed, 2)
            
            # Calculate average distance per ride
            if stats['total_rides'] > 0:
                stats['avg_distance_km'] = round(stats['total_distance_km'] / stats['total_rides'], 2)
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get stats: {str(e)}"
        }), 500


@stats_bp.route('/stats/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Get leaderboard (mock implementation)
    
    Query parameters:
    - metric: Metric to rank by ('distance', 'rides', 'carbon') (default: distance)
    - limit: Number of results (default: 10)
    
    Response:
    {
        "metric": str,
        "rankings": list
    }
    """
    try:
        metric = request.args.get('metric', 'distance')
        limit = request.args.get('limit', type=int, default=10)
        
        # Get all rides
        all_rides = data_store.get_all_rides()
        
        # Group by user
        user_stats = {}
        for ride in all_rides:
            user_id = ride.get('user_id')
            if user_id not in user_stats:
                user_stats[user_id] = {
                    'user_id': user_id,
                    'total_rides': 0,
                    'total_distance': 0,
                    'total_carbon': 0
                }
            
            user_stats[user_id]['total_rides'] += 1
            user_stats[user_id]['total_distance'] += ride.get('distance', 0)
            user_stats[user_id]['total_carbon'] += ride.get('carbon_reduction', 0)
        
        # Convert to list and sort
        rankings = list(user_stats.values())
        
        # Sort by selected metric
        if metric == 'rides':
            rankings.sort(key=lambda x: x['total_rides'], reverse=True)
        elif metric == 'carbon':
            rankings.sort(key=lambda x: x['total_carbon'], reverse=True)
        else:  # distance
            rankings.sort(key=lambda x: x['total_distance'], reverse=True)
        
        # Apply limit
        rankings = rankings[:limit]
        
        # Format output
        formatted_rankings = []
        for i, user in enumerate(rankings, 1):
            formatted_rankings.append({
                'rank': i,
                'user_id': user['user_id'],
                'total_rides': user['total_rides'],
                'total_distance_km': round(user['total_distance'] / 1000, 2),
                'total_carbon_saved_kg': round(user['total_carbon'], 2)
            })
        
        return jsonify({
            'metric': metric,
            'rankings': formatted_rankings
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get leaderboard: {str(e)}"
        }), 500


@stats_bp.route('/stats/weekly', methods=['GET'])
def get_weekly_stats():
    """
    Get weekly statistics (mock implementation)
    
    Query parameters:
    - user_id: Filter by user ID (optional)
    
    Response:
    {
        "period": str,
        "stats": dict
    }
    """
    try:
        user_id = request.args.get('user_id')
        
        # Get all rides for the user
        rides = data_store.get_all_rides(user_id)
        
        # For simplicity, return overall stats
        # In a real implementation, you would filter by date range
        total_rides = len(rides)
        total_distance = sum(ride.get('distance', 0) for ride in rides)
        total_carbon = sum(ride.get('carbon_reduction', 0) for ride in rides)
        total_duration = sum(ride.get('duration', 0) for ride in rides)
        
        return jsonify({
            'period': 'last_7_days',
            'stats': {
                'total_rides': total_rides,
                'total_distance_km': round(total_distance / 1000, 2),
                'total_carbon_saved_kg': round(total_carbon, 2),
                'total_duration_hours': round(total_duration / 3600, 2),
                'avg_rides_per_day': round(total_rides / 7, 1)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get weekly stats: {str(e)}"
        }), 500


@stats_bp.route('/stats/monthly', methods=['GET'])
def get_monthly_stats():
    """
    Get monthly statistics (mock implementation)
    
    Query parameters:
    - user_id: Filter by user ID (optional)
    
    Response:
    {
        "period": str,
        "stats": dict
    }
    """
    try:
        user_id = request.args.get('user_id')
        
        # Get all rides for the user
        rides = data_store.get_all_rides(user_id)
        
        # For simplicity, return overall stats
        # In a real implementation, you would filter by date range
        total_rides = len(rides)
        total_distance = sum(ride.get('distance', 0) for ride in rides)
        total_carbon = sum(ride.get('carbon_reduction', 0) for ride in rides)
        total_duration = sum(ride.get('duration', 0) for ride in rides)
        
        return jsonify({
            'period': 'last_30_days',
            'stats': {
                'total_rides': total_rides,
                'total_distance_km': round(total_distance / 1000, 2),
                'total_carbon_saved_kg': round(total_carbon, 2),
                'total_duration_hours': round(total_duration / 3600, 2),
                'avg_rides_per_day': round(total_rides / 30, 1)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get monthly stats: {str(e)}"
        }), 500


@stats_bp.route('/stats/achievements', methods=['GET'])
def get_achievements():
    """
    Get user achievements (mock implementation)
    
    Query parameters:
    - user_id: User ID (required)
    
    Response:
    {
        "user_id": str,
        "achievements": list
    }
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                "error": "user_id is required"
            }), 400
        
        # Get user stats
        stats = data_store.get_user_stats(user_id)
        
        # Generate achievements based on stats
        achievements = []
        
        # Distance achievements
        if stats['total_distance_km'] >= 100:
            achievements.append({
                'id': 'distance_100',
                'name': '百里征程',
                'description': '累積騎行 100 公里',
                'icon': '🏆',
                'unlocked': True
            })
        
        if stats['total_distance_km'] >= 500:
            achievements.append({
                'id': 'distance_500',
                'name': '千里之行',
                'description': '累積騎行 500 公里',
                'icon': '🌟',
                'unlocked': True
            })
        
        # Ride count achievements
        if stats['total_rides'] >= 10:
            achievements.append({
                'id': 'rides_10',
                'name': '騎行新手',
                'description': '完成 10 次騎行',
                'icon': '🚴',
                'unlocked': True
            })
        
        if stats['total_rides'] >= 50:
            achievements.append({
                'id': 'rides_50',
                'name': '騎行達人',
                'description': '完成 50 次騎行',
                'icon': '🚴‍♂️',
                'unlocked': True
            })
        
        # Carbon reduction achievements
        if stats['total_carbon_saved_kg'] >= 10:
            achievements.append({
                'id': 'carbon_10',
                'name': '環保先鋒',
                'description': '減碳 10 公斤',
                'icon': '🌱',
                'unlocked': True
            })
        
        return jsonify({
            'user_id': user_id,
            'total_achievements': len(achievements),
            'achievements': achievements
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get achievements: {str(e)}"
        }), 500
