# New Weather API Data Structure Quick Reference

## API Endpoint
```
https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-061
```

## Parameters
```
Authorization: CWA-E55648B2-9676-4603-A8A4-6662D8D488BB
format: JSON
ElementName: 天氣預報綜合描述,3小時降雨機率,溫度,天氣現象
LocationName: (optional, district names like 松山區,信義區)
```

## Response Structure
```json
{
  "success": "true",
  "records": {
    "Locations": [
      {
        "LocationsName": "臺北市",
        "Location": [
          {
            "LocationName": "松山區",
            "Geocode": "63000010",
            "Latitude": "25.051608",
            "Longitude": "121.568983",
            "WeatherElement": [
              {
                "ElementName": "溫度",
                "Time": [
                  {
                    "DataTime": "2025-11-09T00:00:00+08:00",
                    "ElementValue": [
                      { "Temperature": "25" }
                    ]
                  }
                ]
              },
              {
                "ElementName": "3小時降雨機率",
                "Time": [
                  {
                    "StartTime": "2025-11-09T00:00:00+08:00",
                    "EndTime": "2025-11-09T03:00:00+08:00",
                    "ElementValue": [
                      { "ProbabilityOfPrecipitation": "10" }
                    ]
                  }
                ]
              },
              {
                "ElementName": "天氣預報綜合描述",
                "Time": [
                  {
                    "StartTime": "2025-11-09T00:00:00+08:00",
                    "EndTime": "2025-11-09T03:00:00+08:00",
                    "ElementValue": [
                      { 
                        "WeatherDescription": "晴。降雨機率10%。溫度攝氏24至25度。舒適。偏東風 平均風速2-3級(每秒4公尺)。相對濕度93至95%。"
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

## Key Differences from Old API

### Old API (F-C0032-001)
- City-level (臺北市, 新北市)
- 36-hour forecast
- Elements: Wx, PoP, CI, MinT, MaxT
- 12-hour periods
- Min/Max temperatures only

### New API (F-D0047-061)
- District-level (松山區, 信義區)
- 3-day forecast
- Elements: 溫度, 3小時降雨機率, 天氣預報綜合描述
- Hourly temperature data
- 3-hour rain probability blocks
- Comprehensive descriptions with wind, humidity, comfort

## Parsing Logic

### Temperature
```python
# Hourly data, find closest to current time
for temp_time in temperature_element["Time"]:
    data_time = temp_time["DataTime"]  # "2025-11-09T04:00:00+08:00"
    temperature = temp_time["ElementValue"][0]["Temperature"]  # "24"
```

### Rain Probability
```python
# 3-hour blocks
for rain_time in rain_element["Time"]:
    start_time = rain_time["StartTime"]  # "2025-11-09T00:00:00+08:00"
    end_time = rain_time["EndTime"]      # "2025-11-09T03:00:00+08:00"
    probability = rain_time["ElementValue"][0]["ProbabilityOfPrecipitation"]  # "10"
```

### Weather Description
```python
# 3-hour blocks with comprehensive info
for desc_time in description_element["Time"]:
    description = desc_time["ElementValue"][0]["WeatherDescription"]
    # Example: "晴。降雨機率10%。溫度攝氏24至25度。舒適。偏東風 平均風速2-3級(每秒4公尺)。相對濕度93至95%。"
```

## Finding Nearest Location

```python
def find_nearest_location(lat, lng):
    """
    Find closest district to given coordinates
    Uses Haversine distance formula
    """
    # Loop through all districts
    for location in all_locations:
        loc_lat = float(location["Latitude"])
        loc_lng = float(location["Longitude"])
        
        # Calculate distance
        distance = haversine_distance(lat, lng, loc_lat, loc_lng)
        
        # Keep track of nearest
        if distance < min_distance:
            min_distance = distance
            nearest = location
    
    return nearest
```

## Backend Route Integration

### Input
```
GET /api/weather?lat=25.0374865&lng=121.5647688&include_aqi=true
```

### Process
1. Fetch all district data from F-D0047-061
2. Find nearest district using coordinates
3. Parse temperature (hourly → find closest to now)
4. Parse rain probability (3-hour blocks → find current block)
5. Extract weather condition from description (first sentence)
6. Extract comfort index from description
7. Find nearest AQI station using same coordinates

### Output
```json
{
  "location": "臺北市",
  "timestamp": "2025-11-09T...",
  "weather": {
    "location_name": "信義區",
    "temperature": "24°C",
    "weather_condition": "陰",
    "rain_probability_3h": "10.0%",
    "comfort_index": "舒適",
    "forecast_period": {
      "start_time": "2025-11-09 06:00:00",
      "end_time": "2025-11-09 09:00:00"
    }
  },
  "aqi": { ... }
}
```

## Taipei City Districts Covered

1. 松山區 (Songshan)
2. 信義區 (Xinyi)
3. 大安區 (Da'an)
4. 中山區 (Zhongshan)
5. 中正區 (Zhongzheng)
6. 大同區 (Datong)
7. 萬華區 (Wanhua)
8. 文山區 (Wenshan)
9. 南港區 (Nangang)
10. 內湖區 (Neihu)
11. 士林區 (Shilin)
12. 北投區 (Beitou)

Each district has its own coordinates and weather data updated every 3 hours.
