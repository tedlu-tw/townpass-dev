#!/usr/bin/env python3
"""
Taiwan Weather Data Fetcher
Fetches weather forecast data from Central Weather Administration (CWA) API
"""

import requests
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class WeatherFetcher:
    """Fetches and processes weather forecast data from CWA"""
    
    BASE_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    
    def __init__(self, locations: List[str] = None, elements: List[str] = None, api_key: str = None):
        """
        Initialize weather fetcher
        
        Args:
            locations: List of location names (default: 臺北市, 新北市, 基隆市)
            elements: List of weather elements (default: Wx, PoP, CI, MinT, MaxT)
            api_key: CWA API key (default: from CWA_API_KEY environment variable)
        """
        self.locations = locations or ["臺北市", "新北市", "基隆市"]
        self.elements = elements or ["Wx", "PoP", "CI", "MinT", "MaxT"]
        self.api_key = api_key or os.getenv("CWA_API_KEY")
        self.data: Optional[Dict] = None
        
        if not self.api_key:
            raise ValueError("CWA_API_KEY not found. Please set it in .env file or pass it as a parameter.")
    
    def fetch_data(self, timeout: int = 10, verify_ssl: bool = True) -> bool:
        """
        Fetch weather data from CWA API
        
        Args:
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificate (default: True)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Build query parameters
            params = {
                "Authorization": self.api_key,
                "format": "JSON",
                "locationName": ",".join(self.locations),
                "elementName": ",".join(self.elements)
            }
            
            print(f"Fetching weather data from CWA API...")
            print(f"Locations: {', '.join(self.locations)}")
            print(f"Elements: {', '.join(self.elements)}")
            
            # Add headers for better compatibility
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(
                self.BASE_URL, 
                params=params, 
                headers=headers,
                timeout=timeout,
                verify=verify_ssl
            )
            response.raise_for_status()
            
            self.data = response.json()
            
            # Check if request was successful
            if self.data.get("success") == "true":
                locations_count = len(self.data.get("records", {}).get("location", []))
                print(f"✓ Successfully fetched weather data for {locations_count} locations")
                return True
            else:
                print(f"✗ API returned success=false")
                return False
            
        except requests.exceptions.Timeout:
            print(f"✗ Error: Request timed out after {timeout} seconds")
            return False
        except requests.exceptions.SSLError as e:
            print(f"✗ SSL Error: {e}")
            print("💡 Tip: Try running with verify_ssl=False or update your SSL certificates")
            print("   On macOS, you may need to run: /Applications/Python*/Install\\ Certificates.command")
            return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching data: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON: {e}")
            return False
    
    def get_location_weather(self, location_name: str) -> Optional[Dict]:
        """Get weather data for a specific location"""
        if not self.data:
            return None
        
        locations = self.data.get("records", {}).get("location", [])
        for location in locations:
            if location.get("locationName") == location_name:
                return location
        return None
    
    def display_weather_summary(self):
        """Display weather summary for all locations"""
        if not self.data:
            print("No data available")
            return
        
        locations = self.data.get("records", {}).get("location", [])
        dataset_desc = self.data.get("records", {}).get("datasetDescription", "N/A")
        
        print("\n" + "="*80)
        print(f"Weather Forecast: {dataset_desc}")
        print("="*80)
        
        for location in locations:
            location_name = location.get("locationName", "Unknown")
            print(f"\n📍 {location_name}")
            print("-" * 80)
            
            weather_elements = location.get("weatherElement", [])
            
            # Get the first time period for each element
            for element in weather_elements:
                element_name = element.get("elementName", "")
                time_data = element.get("time", [])
                
                if time_data:
                    first_period = time_data[0]
                    start_time = first_period.get("startTime", "")
                    end_time = first_period.get("endTime", "")
                    parameter = first_period.get("parameter", {})
                    param_name = parameter.get("parameterName", "")
                    param_unit = parameter.get("parameterUnit", "")
                    
                    # Format element name
                    element_display = {
                        "Wx": "天氣現象 (Weather)",
                        "PoP": "降雨機率 (Rain Probability)",
                        "CI": "舒適度 (Comfort Index)",
                        "MinT": "最低溫度 (Min Temp)",
                        "MaxT": "最高溫度 (Max Temp)"
                    }.get(element_name, element_name)
                    
                    # Format value
                    if param_unit:
                        value_display = f"{param_name} {param_unit}"
                    else:
                        value_display = param_name
                    
                    print(f"  {element_display}: {value_display}")
                    print(f"    Period: {start_time} ~ {end_time}")
        
        print("="*80)
    
    def display_location_detail(self, location_name: str):
        """Display detailed weather information for a specific location"""
        location_data = self.get_location_weather(location_name)
        
        if not location_data:
            print(f"No data found for location: {location_name}")
            return
        
        print("\n" + "="*80)
        print(f"Detailed Weather Forecast: {location_name}")
        print("="*80)
        
        weather_elements = location_data.get("weatherElement", [])
        
        for element in weather_elements:
            element_name = element.get("elementName", "")
            element_display = {
                "Wx": "天氣現象 (Weather Condition)",
                "PoP": "降雨機率 (Probability of Precipitation)",
                "CI": "舒適度 (Comfort Index)",
                "MinT": "最低溫度 (Minimum Temperature)",
                "MaxT": "最高溫度 (Maximum Temperature)"
            }.get(element_name, element_name)
            
            print(f"\n{element_display}:")
            print("-" * 80)
            
            time_data = element.get("time", [])
            for i, period in enumerate(time_data, 1):
                start_time = period.get("startTime", "")
                end_time = period.get("endTime", "")
                parameter = period.get("parameter", {})
                param_name = parameter.get("parameterName", "")
                param_unit = parameter.get("parameterUnit", "")
                
                value_display = f"{param_name} {param_unit}" if param_unit else param_name
                
                print(f"  Period {i}: {start_time} ~ {end_time}")
                print(f"    Value: {value_display}")
        
        print("="*80)
    
    def save_to_file(self, filename: str = "weather_data.json", output_dir: str = "data"):
        """Save fetched data to a JSON file"""
        if not self.data:
            print("No data to save")
            return False
        
        try:
            # Create output directory if it doesn't exist
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Full path to the output file
            file_path = output_path / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"✓ Data saved to {file_path}")
            return True
        except Exception as e:
            print(f"✗ Error saving to file: {e}")
            return False
    
    def get_rain_alerts(self, threshold: int = 30) -> List[Dict]:
        """
        Get locations and time periods with rain probability above threshold
        
        Args:
            threshold: Rain probability threshold (default: 30%)
            
        Returns:
            List of rain alerts
        """
        if not self.data:
            return []
        
        alerts = []
        locations = self.data.get("records", {}).get("location", [])
        
        for location in locations:
            location_name = location.get("locationName", "")
            weather_elements = location.get("weatherElement", [])
            
            # Find PoP (Probability of Precipitation) element
            for element in weather_elements:
                if element.get("elementName") == "PoP":
                    time_data = element.get("time", [])
                    for period in time_data:
                        parameter = period.get("parameter", {})
                        pop_value = int(parameter.get("parameterName", "0"))
                        
                        if pop_value >= threshold:
                            alerts.append({
                                "location": location_name,
                                "startTime": period.get("startTime"),
                                "endTime": period.get("endTime"),
                                "rainProbability": pop_value
                            })
        
        return alerts


def main():
    """Main function demonstrating usage"""
    # Initialize fetcher with default locations and elements
    fetcher = WeatherFetcher()
    
    # Fetch data (try with SSL verification first, then without if it fails)
    if not fetcher.fetch_data(verify_ssl=True):
        print("\n⚠️  Retrying without SSL verification...")
        if not fetcher.fetch_data(verify_ssl=False):
            return
    
    # Display weather summary
    fetcher.display_weather_summary()
    
    # Display detailed forecast for Taipei City
    print("\n")
    fetcher.display_location_detail("臺北市")
    
    # Check for rain alerts (PoP >= 30%)
    print("\n")
    rain_alerts = fetcher.get_rain_alerts(threshold=30)
    if rain_alerts:
        print("⚠️  Rain Alerts (Probability ≥ 30%):")
        print("="*80)
        for alert in rain_alerts:
            print(f"  {alert['location']}: {alert['rainProbability']}% chance of rain")
            print(f"    {alert['startTime']} ~ {alert['endTime']}")
    else:
        print("☀️  No significant rain expected")
    
    # Save data to file
    print("\n")
    fetcher.save_to_file("weather_data.json")


if __name__ == "__main__":
    main()
