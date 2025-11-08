"""
Weather Routes - Handle weather and AQI data
GET /weather - Get current weather and AQI information
Uses CWA API F-D0047-061 for district-level 3-day forecasts
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
    """Parse weather data from new F-D0047-061 API format"""
    if not weather_data:
        return None
    
    parsed = {
        "location_name": weather_data.get("LocationName"),
        "forecast_periods": []
    }
    
    weather_elements = weather_data.get("WeatherElement", [])
    
    # Get temperature, rain probability, and weather description elements
    temp_element = None
    rain_element = None
    desc_element = None
    
    for element in weather_elements:
        element_name = element.get("ElementName")
        if element_name == "溫度":
            temp_element = element
        elif element_name == "3小時降雨機率":
            rain_element = element
        elif element_name == "天氣預報綜合描述":
            desc_element = element
    
    # Parse 3-hour rain probability periods
    if rain_element:
        time_periods = rain_element.get("Time", [])
        for time_period in time_periods:
            period_data = {
                "start_time": time_period.get("StartTime", "").replace("+08:00", "").replace("T", " "),
                "end_time": time_period.get("EndTime", "").replace("+08:00", "").replace("T", " ")
            }
            
            # Get rain probability
            element_values = time_period.get("ElementValue", [])
            if element_values:
                try:
                    period_data["rain_probability"] = int(element_values[0].get("ProbabilityOfPrecipitation", 0))
                except (ValueError, TypeError):
                    period_data["rain_probability"] = 0
            
            # Get weather description for this period
            if desc_element:
                desc_times = desc_element.get("Time", [])
                for desc_time in desc_times:
                    if desc_time.get("StartTime") == time_period.get("StartTime"):
                        desc_values = desc_time.get("ElementValue", [])
                        if desc_values:
                            period_data["weather_description"] = desc_values[0].get("WeatherDescription", "")
                        break
            
            parsed["forecast_periods"].append(period_data)
    
    # Store temperature data separately (hourly)
    if temp_element:
        temp_times = temp_element.get("Time", [])
        parsed["temperature_data"] = []
        for temp_time in temp_times:
            data_time = temp_time.get("DataTime", "").replace("+08:00", "").replace("T", " ")
            element_values = temp_time.get("ElementValue", [])
            if element_values:
                try:
                    temp = int(element_values[0].get("Temperature", 0))
                    parsed["temperature_data"].append({
                        "time": data_time,
                        "temperature": temp
                    })
                except (ValueError, TypeError):
                    pass
    
    return parsed


def get_current_temperature(temperature_data):
    """Get current temperature from hourly temperature data"""
    if not temperature_data:
        return None
    
    from datetime import datetime
    current_time = datetime.now()
    
    # Find the closest temperature reading to current time
    closest_temp = None
    min_time_diff = float('inf')
    
    for temp_record in temperature_data:
        try:
            temp_time_str = temp_record.get("time", "")
            temp_time = datetime.strptime(temp_time_str, "%Y-%m-%d %H:%M:%S")
            time_diff = abs((temp_time - current_time).total_seconds())
            
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_temp = temp_record.get("temperature")
        except Exception:
            continue
    
    return closest_temp


def calculate_average_pop_next_3_hours(forecast_periods):
    """Calculate average precipitation probability for next 3 hours"""
    if not forecast_periods:
        return 0
    
    current_time = datetime.now()
    
    # Find current 3-hour period
    for period in forecast_periods:
        try:
            start_time_str = period.get("start_time", "")
            end_time_str = period.get("end_time", "")
            
            if start_time_str and end_time_str:
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
                
                # Check if current time is within this 3-hour period
                if start_time <= current_time <= end_time:
                    pop = period.get("rain_probability", 0)
                    return float(pop) if isinstance(pop, (int, float)) else 0
        except Exception:
            continue
    
    # If no matching period found, return first period's value
    if forecast_periods:
        pop = forecast_periods[0].get("rain_probability", 0)
        return float(pop) if isinstance(pop, (int, float)) else 0
    
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
    Get current weather and AQI data using coordinates
    
    Query parameters:
    - location: Location name (default: 臺北市) - not used with new API
    - lat: Latitude (recommended, for finding nearest weather district)
    - lng: Longitude (recommended, for finding nearest weather district)
    - include_aqi: Include AQI data (default: true)
    
    Response:
    {
        "location": str,
        "timestamp": str,
        "weather": {
            "location_name": str,                  # District name (e.g., 松山區)
            "temperature": str,                    # Current temperature from hourly data
            "weather_condition": str,              # Weather description (e.g., 晴, 多雲)
            "rain_probability_3h": str,            # Current 3-hour rain probability
            "comfort_index": str,                  # Comfort index (舒適, 悶熱, etc.)
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
            weather_fetcher_instance = WeatherFetcher()
            if weather_fetcher_instance.fetch_data(verify_ssl=False):
                # If lat/lng provided, find nearest location
                if lat is not None and lng is not None:
                    weather_raw = weather_fetcher_instance.find_nearest_location(lat, lng)
                else:
                    # Fallback to location name search (not reliable with new API)
                    weather_raw = weather_fetcher_instance.get_location_weather(location)
                
                if weather_raw:
                    parsed_weather = parse_weather_data(weather_raw)
                    if parsed_weather and parsed_weather.get("forecast_periods"):
                        # Get current period (first forecast period)
                        current_period = parsed_weather["forecast_periods"][0]
                        
                        # Get current temperature from hourly data
                        current_temp = get_current_temperature(parsed_weather.get("temperature_data", []))
                        
                        # Calculate average PoP for next 3 hours
                        avg_pop_3h = calculate_average_pop_next_3_hours(parsed_weather["forecast_periods"])
                        
                        # Extract weather condition from description
                        weather_desc = current_period.get("weather_description", "")
                        weather_condition = weather_desc.split("。")[0] if weather_desc else "N/A"
                        
                        # Extract comfort from description
                        comfort_index = "舒適"
                        if "舒適" in weather_desc:
                            comfort_index = "舒適"
                        elif "悶熱" in weather_desc:
                            comfort_index = "悶熱"
                        elif "寒冷" in weather_desc:
                            comfort_index = "寒冷"
                        
                        response_data["weather"] = {
                            "location_name": parsed_weather["location_name"],
                            "temperature": f"{current_temp}°C" if current_temp else "N/A",
                            "weather_condition": weather_condition,
                            "rain_probability_3h": f"{avg_pop_3h}%",
                            "comfort_index": comfort_index,
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
