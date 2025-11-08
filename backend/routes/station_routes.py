"""
Station Routes - Handle YouBike station operations
GET /nearby - Get nearby YouBike stations
GET /<station_id> - Get specific station info
"""

from flask import Blueprint, request, jsonify
from scripts.fetch_youbike_data import YouBikeFetcher
import math

station_bp = Blueprint('station', __name__)

# Initialize YouBike fetcher
youbike_fetcher = YouBikeFetcher()


def determine_station_color(station):
    """
    Determine station marker color based on availability
    
    Args:
        station: Station data dict
    
    Returns:
        Color string: 'green', 'yellow', or 'red'
    """
    available_rent = station.get('available_rent_bikes', 0)
    available_return = station.get('available_return_bikes', 0)
    
    # Red: No docks available
    if available_return == 0:
        return 'red'
    # Yellow: No bikes available
    elif available_rent == 0:
        return 'yellow'
    # Green: Both available
    else:
        return 'green'


def station_to_geojson_feature(station, include_distance=False):
    """
    Convert station data to GeoJSON Feature format
    
    Args:
        station: Station data dict
        include_distance: Whether to include distance in properties
    
    Returns:
        GeoJSON Feature dict
    """
    # Remove "YouBike2.0_" prefix from station name
    station_name = station.get('sna', '')
    if station_name.startswith('YouBike2.0_'):
        station_name = station_name.replace('YouBike2.0_', '', 1)
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                float(station.get('longitude', 0)),
                float(station.get('latitude', 0))
            ]
        },
        "properties": {
            "id": station.get('sno'),
            "name": station_name,
            "site": station.get('ar', ''),
            "icon": determine_station_color(station),
            "available_bikes": station.get('available_rent_bikes', 0),
            "available_docks": station.get('available_return_bikes', 0),
            "area": station.get('sarea', ''),
            "update_time": station.get('updateTime', ''),
            "active": station.get('act') == '1'
        }
    }
    
    # Add distance if provided
    if include_distance and 'distance' in station:
        feature['properties']['distance'] = station['distance']
    
    return feature


def stations_to_geojson(stations, include_distance=False):
    """
    Convert list of stations to GeoJSON FeatureCollection
    
    Args:
        stations: List of station data dicts
        include_distance: Whether to include distance in properties
    
    Returns:
        GeoJSON FeatureCollection dict
    """
    return {
        "type": "FeatureCollection",
        "features": [
            station_to_geojson_feature(station, include_distance)
            for station in stations
        ]
    }


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula
    
    Args:
        lat1, lon1: First coordinate
        lat2, lon2: Second coordinate
    
    Returns:
        Distance in meters
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in meters
    r = 6371000
    
    return c * r


@station_bp.route('/nearby', methods=['GET'])
def get_nearby_stations():
    """
    Get nearby YouBike stations based on coordinates
    
    Query parameters:
    - lat: Latitude (required)
    - lng: Longitude (required)
    - radius: Search radius in meters (default: 1000)
    - limit: Maximum number of results (default: 10)
    - type: Filter by 'available' (has bikes) or 'empty' (has spaces) (optional)
    - min_bikes: Minimum available bikes (default: 1)
    
    Response:
    {
        "count": int,
        "stations": list,
        "query": dict
    }
    """
    try:
        # Get query parameters
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', type=float, default=1000)  # meters
        limit = request.args.get('limit', type=int, default=10)
        station_type = request.args.get('type')
        min_bikes = request.args.get('min_bikes', type=int, default=1)
        
        # Validate required parameters
        if lat is None or lng is None:
            return jsonify({
                "error": "Missing required parameters",
                "message": "Both 'lat' and 'lng' are required"
            }), 400
        
        # Fetch YouBike data
        if not youbike_fetcher.fetch_data():
            return jsonify({
                "error": "Failed to fetch YouBike data",
                "message": "Unable to retrieve station information"
            }), 503
        
        # Get all stations
        all_stations = youbike_fetcher.data
        
        if not all_stations:
            return jsonify({
                "count": 0,
                "stations": [],
                "message": "No stations available"
            }), 200
        
        # Calculate distances and filter
        nearby_stations = []
        
        for station in all_stations:
            try:
                station_lat = float(station.get('latitude', 0))
                station_lng = float(station.get('longitude', 0))
                
                # Calculate distance
                distance = calculate_distance(lat, lng, station_lat, station_lng)
                
                # Filter by radius
                if distance <= radius:
                    # Add distance to station data
                    station_with_distance = station.copy()
                    station_with_distance['distance'] = round(distance, 2)
                    
                    # Filter by type if specified
                    if station_type == 'available':
                        if station.get('available_rent_bikes', 0) >= min_bikes:
                            nearby_stations.append(station_with_distance)
                    elif station_type == 'empty':
                        if station.get('available_return_bikes', 0) > 0:
                            nearby_stations.append(station_with_distance)
                    else:
                        nearby_stations.append(station_with_distance)
            
            except (ValueError, TypeError):
                # Skip stations with invalid coordinates
                continue
        
        # Sort by distance
        nearby_stations.sort(key=lambda x: x['distance'])
        
        # Apply limit
        nearby_stations = nearby_stations[:limit]
        
        # Convert to GeoJSON
        geojson = stations_to_geojson(nearby_stations, include_distance=True)
        
        # Add metadata
        geojson['metadata'] = {
            "count": len(nearby_stations),
            "query": {
                "lat": lat,
                "lng": lng,
                "radius": radius,
                "type": station_type
            }
        }
        
        return jsonify(geojson), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get nearby stations: {str(e)}"}), 500


@station_bp.route('/<station_id>', methods=['GET'])
def get_station_info(station_id):
    """
    Get specific station information
    
    Path parameters:
    - station_id: Station ID (sno)
    
    Response:
    {
        "station": dict
    }
    """
    try:
        # Fetch YouBike data
        if not youbike_fetcher.fetch_data():
            return jsonify({
                "error": "Failed to fetch YouBike data",
                "message": "Unable to retrieve station information"
            }), 503
        
        # Get station by ID
        station = youbike_fetcher.get_station_by_sno(station_id)
        
        if not station:
            return jsonify({
                "error": "Station not found",
                "station_id": station_id
            }), 404
        
        # Convert to GeoJSON Feature
        geojson_feature = station_to_geojson_feature(station)
        
        return jsonify(geojson_feature), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get station info: {str(e)}"}), 500


@station_bp.route('/area/<area_name>', methods=['GET'])
def get_stations_by_area(area_name):
    """
    Get all stations in a specific area
    
    Path parameters:
    - area_name: Area name (e.g., "中正區", "Zhongzheng Dist.")
    
    Response:
    {
        "count": int,
        "area": str,
        "stations": list
    }
    """
    try:
        # Fetch YouBike data
        if not youbike_fetcher.fetch_data():
            return jsonify({
                "error": "Failed to fetch YouBike data",
                "message": "Unable to retrieve station information"
            }), 503
        
        # Get stations by area
        stations = youbike_fetcher.get_stations_by_area(area_name)
        
        # Convert to GeoJSON
        geojson = stations_to_geojson(stations)
        
        # Add metadata
        geojson['metadata'] = {
            "count": len(stations),
            "area": area_name
        }
        
        return jsonify(geojson), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get stations by area: {str(e)}"}), 500


@station_bp.route('/available', methods=['GET'])
def get_available_stations():
    """
    Get all stations with available bikes
    
    Query parameters:
    - min_bikes: Minimum number of available bikes (default: 1)
    - limit: Maximum number of results (optional)
    
    Response:
    {
        "count": int,
        "stations": list
    }
    """
    try:
        min_bikes = request.args.get('min_bikes', type=int, default=1)
        limit = request.args.get('limit', type=int)
        
        # Fetch YouBike data
        if not youbike_fetcher.fetch_data():
            return jsonify({
                "error": "Failed to fetch YouBike data",
                "message": "Unable to retrieve station information"
            }), 503
        
        # Get available stations
        stations = youbike_fetcher.get_available_stations(min_bikes)
        
        # Apply limit if specified
        if limit and limit > 0:
            stations = stations[:limit]
        
        # Convert to GeoJSON
        geojson = stations_to_geojson(stations)
        
        # Add metadata
        geojson['metadata'] = {
            "count": len(stations),
            "min_bikes": min_bikes
        }
        
        return jsonify(geojson), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get available stations: {str(e)}"}), 500


@station_bp.route('/stats', methods=['GET'])
def get_station_stats():
    """
    Get overall station statistics
    
    Response:
    {
        "total_stations": int,
        "active_stations": int,
        "total_bikes": int,
        "total_spaces": int,
        "update_time": str
    }
    """
    try:
        # Fetch YouBike data
        if not youbike_fetcher.fetch_data():
            return jsonify({
                "error": "Failed to fetch YouBike data",
                "message": "Unable to retrieve station information"
            }), 503
        
        all_stations = youbike_fetcher.data
        
        if not all_stations:
            return jsonify({
                "error": "No station data available"
            }), 503
        
        # Calculate statistics
        total_stations = len(all_stations)
        active_stations = sum(1 for s in all_stations if s.get('act') == '1')
        total_bikes = sum(s.get('available_rent_bikes', 0) for s in all_stations)
        total_spaces = sum(s.get('available_return_bikes', 0) for s in all_stations)
        
        # Get latest update time
        update_times = [s.get('updateTime') for s in all_stations if s.get('updateTime')]
        latest_update = max(update_times) if update_times else None
        
        return jsonify({
            "total_stations": total_stations,
            "active_stations": active_stations,
            "total_bikes": total_bikes,
            "total_spaces": total_spaces,
            "update_time": latest_update
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get station stats: {str(e)}"}), 500
