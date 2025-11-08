"""
Weather Routes - Handle weather and AQI data
GET /weather - Get current weather and AQI information
"""

from flask import Blueprint, request, jsonify
from scripts.fetch_weather_data import WeatherFetcher
from scripts.fetch_aqi_data import AQIFetcher
from datetime import datetime

weather_bp = Blueprint('weather', __name__)

# Initialize fetchers
weather_fetcher = WeatherFetcher()
aqi_fetcher = AQIFetcher()


def parse_weather_data(weather_data):
    """Parse weather data to extract key information"""
    if not weather_data:
        return None
    
    parsed = {
        "location_name": weather_data.get("locationName"),
        "forecast_periods": []
    }
    
    weather_elements = weather_data.get("weatherElement", [])
    
    # Get all time periods from the first element
    if weather_elements:
        time_periods = weather_elements[0].get("time", [])
        
        for time_index, time_period in enumerate(time_periods):
            period_data = {
                "start_time": time_period.get("startTime"),
                "end_time": time_period.get("endTime")
            }
            
            # Extract data for each element at this time period
            for element in weather_elements:
                element_name = element.get("elementName")
                times = element.get("time", [])
                
                if time_index < len(times):
                    parameter = times[time_index].get("parameter", {})
                    param_name = parameter.get("parameterName")
                    param_unit = parameter.get("parameterUnit")
                    
                    if element_name == "Wx":
                        period_data["weather_condition"] = param_name
                    elif element_name == "PoP":
                        # Store as integer for averaging calculation
                        try:
                            period_data["rain_probability"] = int(param_name)
                        except (ValueError, TypeError):
                            period_data["rain_probability"] = 0
                    elif element_name == "MinT":
                        period_data["min_temperature"] = param_name
                    elif element_name == "MaxT":
                        period_data["max_temperature"] = param_name
                    elif element_name == "CI":
                        period_data["comfort_index"] = param_name
            
            parsed["forecast_periods"].append(period_data)
    
    return parsed


def calculate_current_temperature(period):
    """Calculate current temperature from min/max"""
    try:
        min_temp = float(period.get("min_temperature", 0))
        max_temp = float(period.get("max_temperature", 0))
        # Return average of min and max as current estimate
        current_temp = (min_temp + max_temp) / 2
        return round(current_temp, 1)
    except (ValueError, TypeError):
        return None


def calculate_average_pop_next_3_hours(forecast_periods):
    """Calculate average precipitation probability for next 3 hours"""
    if not forecast_periods:
        return 0
    
    pop_values = []
    current_time = datetime.now()
    
    for period in forecast_periods:
        try:
            start_time_str = period.get("start_time", "")
            if start_time_str:
                # Parse the start time
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                
                # Check if this period is within the next 3 hours
                time_diff = (start_time - current_time).total_seconds() / 3600  # hours
                
                if -12 <= time_diff <= 3:  # Include current period and next 3 hours
                    pop = period.get("rain_probability", 0)
                    if isinstance(pop, (int, float)):
                        pop_values.append(pop)
        except Exception:
            continue
    
    # Calculate average
    if pop_values:
        avg_pop = sum(pop_values) / len(pop_values)
        return round(avg_pop, 1)
    
    return 0


def get_aqi_level_name(aqi_value):
    """Get AQI level name based on value"""
    try:
        aqi = int(aqi_value)
        if aqi <= 50:
            return "良好 (Good)"
        elif aqi <= 100:
            return "普通 (Moderate)"
        elif aqi <= 150:
            return "對敏感族群不健康 (Unhealthy for Sensitive Groups)"
        elif aqi <= 200:
            return "對所有族群不健康 (Unhealthy)"
        elif aqi <= 300:
            return "非常不健康 (Very Unhealthy)"
        else:
            return "危害 (Hazardous)"
    except (ValueError, TypeError):
        return "未知 (Unknown)"


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula (in meters)"""
    import math
    
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


def find_nearest_aqi_station(aqi_fetcher, lat, lng):
    """Find the nearest AQI monitoring station to given coordinates"""
    if not aqi_fetcher.data:
        return None
    
    all_stations = aqi_fetcher.data.get("records", [])
    if not all_stations:
        return None
    
    nearest_station = None
    min_distance = float('inf')
    
    for station in all_stations:
        try:
            station_lat = float(station.get('latitude', 0))
            station_lon = float(station.get('longitude', 0))
            
            if station_lat == 0 or station_lon == 0:
                continue
            
            distance = calculate_distance(lat, lng, station_lat, station_lon)
            
            if distance < min_distance:
                min_distance = distance
                nearest_station = station
        except (ValueError, TypeError):
            continue
    
    return nearest_station


def format_aqi_data(aqi_station):
    """Format AQI data with level names"""
    if not aqi_station:
        return None
    
    aqi_value = aqi_station.get('aqi', 'N/A')
    
    return {
        "site_name": aqi_station.get('sitename', 'N/A'),
        "county": aqi_station.get('county', 'N/A'),
        "aqi": aqi_value,
        "aqi_level": get_aqi_level_name(aqi_value),
        "status": aqi_station.get('status', 'N/A'),
        "pm25": aqi_station.get('pm2.5', 'N/A'),
        "pollutant": aqi_station.get('pollutant', 'N/A'),
        "publish_time": aqi_station.get('publishtime', 'N/A')
    }


@weather_bp.route('/weather', methods=['GET'])
def get_weather():
    """
    Get current weather and AQI data
    
    Query parameters:
    - location: Location name (default: 臺北市)
    - lat: Latitude (optional, for finding nearest AQI station)
    - lng: Longitude (optional, for finding nearest AQI station)
    - include_aqi: Include AQI data (default: true)
    
    Response:
    {
        "location": str,
        "timestamp": str,
        "weather": {
            "location_name": str,
            "temperature": str,                    # Current temperature (average of min/max)
            "weather_condition": str,              # Wx (weather condition)
            "rain_probability_3h": str,            # PoP averaged over next 3 hours
            "comfort_index": str,                  # CI (comfort index)
            "forecast_period": {
                "start_time": str,
                "end_time": str
            }
        },
        "aqi": {
            "site_name": str,
            "county": str,
            "aqi": str,
            "aqi_level": str,                      # AQI level with Chinese and English names
            "status": str,
            "pm25": str,
            "pollutant": str,
            "publish_time": str
        }
    }
    """
    try:
        # Get query parameters
        location = request.args.get('location', '臺北市')
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        include_aqi = request.args.get('include_aqi', 'true').lower() == 'true'
        
        response_data = {
            "location": location,
            "timestamp": datetime.now().isoformat()
        }
        
        # Fetch weather data
        try:
            weather_fetcher_instance = WeatherFetcher(locations=[location])
            if weather_fetcher_instance.fetch_data(verify_ssl=False):
                weather_raw = weather_fetcher_instance.get_location_weather(location)
                if weather_raw:
                    parsed_weather = parse_weather_data(weather_raw)
                    if parsed_weather and parsed_weather.get("forecast_periods"):
                        # Get current period (first forecast period)
                        current_period = parsed_weather["forecast_periods"][0]
                        
                        # Calculate current temperature from min/max
                        current_temp = calculate_current_temperature(current_period)
                        
                        # Calculate average PoP for next 3 hours
                        avg_pop_3h = calculate_average_pop_next_3_hours(parsed_weather["forecast_periods"])
                        
                        response_data["weather"] = {
                            "location_name": parsed_weather["location_name"],
                            "temperature": f"{current_temp}°C" if current_temp else "N/A",
                            "weather_condition": current_period.get("weather_condition", "N/A"),
                            "rain_probability_3h": f"{avg_pop_3h}%",
                            "comfort_index": current_period.get("comfort_index", "N/A"),
                            "forecast_period": {
                                "start_time": current_period.get("start_time"),
                                "end_time": current_period.get("end_time")
                            }
                        }
                    else:
                        response_data["weather"] = {
                            "error": "Unable to parse weather data"
                        }
                else:
                    response_data["weather"] = {
                        "error": "Weather data not available for this location"
                    }
            else:
                response_data["weather"] = {
                    "error": "Failed to fetch weather data"
                }
        except Exception as e:
            response_data["weather"] = {
                "error": f"Weather fetch error: {str(e)}"
            }
        
        # Fetch AQI data if requested
        if include_aqi:
            try:
                if aqi_fetcher.fetch_data(verify_ssl=False):
                    # If coordinates provided, find nearest station
                    if lat is not None and lng is not None:
                        nearest_station = find_nearest_aqi_station(aqi_fetcher, lat, lng)
                        if nearest_station:
                            response_data["aqi"] = format_aqi_data(nearest_station)
                        else:
                            response_data["aqi"] = {
                                "message": "No AQI station found near the provided coordinates"
                            }
                    else:
                        # Fallback to county-based lookup
                        aqi_stations = aqi_fetcher.get_stations_by_county(location)
                        if aqi_stations and len(aqi_stations) > 0:
                            # Return formatted data from first station
                            response_data["aqi"] = format_aqi_data(aqi_stations[0])
                        else:
                            # Try to get by site name
                            aqi_station = aqi_fetcher.get_station_by_name(location)
                            if aqi_station:
                                response_data["aqi"] = format_aqi_data(aqi_station)
                            else:
                                response_data["aqi"] = {
                                    "message": "No AQI data available for this location"
                                }
                else:
                    response_data["aqi"] = {
                        "error": "Failed to fetch AQI data"
                    }
            except Exception as e:
                response_data["aqi"] = {
                    "error": f"AQI fetch error: {str(e)}"
                }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get weather data: {str(e)}"
        }), 500
