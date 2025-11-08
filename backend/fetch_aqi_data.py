#!/usr/bin/env python3
"""
Taiwan AQI Data Fetcher
Fetches real-time Air Quality Index (AQI) data from Taiwan Ministry of Environment API
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


class AQIFetcher:
    """Fetches and processes Air Quality Index (AQI) data from MOENV"""
    
    BASE_URL = "https://data.moenv.gov.tw/api/v2/aqx_p_432"
    
    # AQI status definitions
    AQI_LEVELS = {
        (0, 50): {"status": "良好", "color": "green", "description": "空氣質量令人滿意"},
        (51, 100): {"status": "普通", "color": "yellow", "description": "空氣質量可接受"},
        (101, 150): {"status": "對敏感族群不健康", "color": "orange", "description": "敏感族群可能受影響"},
        (151, 200): {"status": "對所有族群不健康", "color": "red", "description": "所有人可能受影響"},
        (201, 300): {"status": "非常不健康", "color": "purple", "description": "健康警報"},
        (301, 500): {"status": "危害", "color": "maroon", "description": "緊急狀態"}
    }
    
    def __init__(self, api_key: str = None, language: str = "zh"):
        """
        Initialize AQI fetcher
        
        Args:
            api_key: MOENV API key (default: from MOENV_API_KEY environment variable)
            language: Response language (default: zh for Chinese)
        """
        self.api_key = api_key or os.getenv("MOENV_API_KEY")
        self.language = language
        self.data: Optional[Dict] = None
        
        if not self.api_key:
            raise ValueError("MOENV_API_KEY not found. Please set it in .env file or pass it as a parameter.")
    
    def fetch_data(self, timeout: int = 10, verify_ssl: bool = True) -> bool:
        """
        Fetch AQI data from MOENV API
        
        Args:
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificate (default: True)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Build query parameters
            params = {
                "api_key": self.api_key,
                "language": self.language
            }
            
            print(f"Fetching AQI data from MOENV API...")
            
            # Add headers
            headers = {
                'accept': '*/*',
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
            
            # Get number of records
            total_records = self.data.get("total", 0)
            records_count = len(self.data.get("records", []))
            
            print(f"✓ Successfully fetched AQI data for {records_count} monitoring stations (Total: {total_records})")
            return True
            
        except requests.exceptions.Timeout:
            print(f"✗ Error: Request timed out after {timeout} seconds")
            return False
        except requests.exceptions.SSLError as e:
            print(f"✗ SSL Error: {e}")
            print("💡 Tip: Try running with verify_ssl=False or update your SSL certificates")
            return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching data: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON: {e}")
            return False
    
    def get_station_by_name(self, sitename: str) -> Optional[Dict]:
        """Get AQI data for a specific monitoring station"""
        if not self.data:
            return None
        
        records = self.data.get("records", [])
        for record in records:
            if record.get("sitename") == sitename:
                return record
        return None
    
    def get_stations_by_county(self, county: str) -> List[Dict]:
        """Get all monitoring stations in a specific county"""
        if not self.data:
            return []
        
        records = self.data.get("records", [])
        return [r for r in records if r.get("county") == county]
    
    def get_unhealthy_stations(self, aqi_threshold: int = 100) -> List[Dict]:
        """
        Get stations with AQI above threshold
        
        Args:
            aqi_threshold: AQI threshold (default: 100)
            
        Returns:
            List of stations with unhealthy air quality
        """
        if not self.data:
            return []
        
        unhealthy = []
        records = self.data.get("records", [])
        
        for record in records:
            aqi_str = record.get("aqi", "")
            if aqi_str and aqi_str.isdigit():
                aqi_value = int(aqi_str)
                if aqi_value >= aqi_threshold:
                    unhealthy.append(record)
        
        return unhealthy
    
    def get_aqi_level(self, aqi_value: int) -> Dict:
        """Get AQI level information based on value"""
        for (min_val, max_val), level_info in self.AQI_LEVELS.items():
            if min_val <= aqi_value <= max_val:
                return level_info
        return {"status": "超標", "color": "black", "description": "數值異常"}
    
    def display_station(self, record: Dict):
        """Display detailed information for a monitoring station"""
        print("\n" + "="*80)
        print(f"測站: {record.get('sitename', 'N/A')} ({record.get('county', 'N/A')})")
        print("="*80)
        
        # AQI and Status
        aqi = record.get('aqi', 'N/A')
        status = record.get('status', 'N/A')
        pollutant = record.get('pollutant', '無')
        print(f"空氣品質指標 (AQI): {aqi}")
        print(f"狀態: {status}")
        if pollutant:
            print(f"主要污染物: {pollutant}")
        
        print("\n污染物濃度:")
        print("-" * 80)
        print(f"  PM2.5 (細懸浮微粒): {record.get('pm2.5', 'N/A')} μg/m³ (移動平均: {record.get('pm2.5_avg', 'N/A')})")
        print(f"  PM10 (懸浮微粒): {record.get('pm10', 'N/A')} μg/m³ (移動平均: {record.get('pm10_avg', 'N/A')})")
        print(f"  O3 (臭氧): {record.get('o3', 'N/A')} ppb (8小時平均: {record.get('o3_8hr', 'N/A')})")
        print(f"  CO (一氧化碳): {record.get('co', 'N/A')} ppm (8小時平均: {record.get('co_8hr', 'N/A')})")
        print(f"  SO2 (二氧化硫): {record.get('so2', 'N/A')} ppb (移動平均: {record.get('so2_avg', 'N/A')})")
        print(f"  NO2 (二氧化氮): {record.get('no2', 'N/A')} ppb")
        print(f"  NO (一氧化氮): {record.get('no', 'N/A')} ppb")
        print(f"  NOx (氮氧化物): {record.get('nox', 'N/A')} ppb")
        
        print("\n氣象資訊:")
        print("-" * 80)
        print(f"  風速: {record.get('wind_speed', 'N/A')} m/sec")
        print(f"  風向: {record.get('wind_direc', 'N/A')}°")
        
        print("\n位置資訊:")
        print("-" * 80)
        print(f"  經度: {record.get('longitude', 'N/A')}")
        print(f"  緯度: {record.get('latitude', 'N/A')}")
        print(f"  測站編號: {record.get('siteid', 'N/A')}")
        
        print(f"\n資料發布時間: {record.get('publishtime', 'N/A')}")
        print("="*80)
    
    def display_summary(self):
        """Display summary statistics"""
        if not self.data:
            print("No data available")
            return
        
        records = self.data.get("records", [])
        total_stations = len(records)
        
        # Count by status
        status_count = {}
        aqi_values = []
        
        for record in records:
            status = record.get('status', '未知')
            status_count[status] = status_count.get(status, 0) + 1
            
            aqi_str = record.get('aqi', '')
            if aqi_str and aqi_str.isdigit():
                aqi_values.append(int(aqi_str))
        
        print("\n" + "="*80)
        print("空氣品質監測站總覽")
        print("="*80)
        print(f"總測站數: {total_stations}")
        
        if aqi_values:
            print(f"平均 AQI: {sum(aqi_values) / len(aqi_values):.1f}")
            print(f"最高 AQI: {max(aqi_values)}")
            print(f"最低 AQI: {min(aqi_values)}")
        
        print("\n依狀態分類:")
        print("-" * 80)
        for status, count in sorted(status_count.items()):
            print(f"  {status}: {count} 站")
        
        print("="*80)
    
    def display_county_summary(self, county: str):
        """Display summary for a specific county"""
        stations = self.get_stations_by_county(county)
        
        if not stations:
            print(f"No stations found in {county}")
            return
        
        print("\n" + "="*80)
        print(f"{county} 空氣品質概況")
        print("="*80)
        print(f"測站數量: {len(stations)}\n")
        
        for station in stations:
            aqi = station.get('aqi', 'N/A')
            status = station.get('status', 'N/A')
            sitename = station.get('sitename', 'N/A')
            pollutant = station.get('pollutant', '')
            
            pollutant_str = f" ({pollutant})" if pollutant else ""
            print(f"  {sitename:8s} - AQI: {aqi:3s} | 狀態: {status}{pollutant_str}")
        
        print("="*80)
    
    def save_to_file(self, filename: str = "aqi_data.json", output_dir: str = "data"):
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


def main():
    """Main function demonstrating usage"""
    # Initialize fetcher
    fetcher = AQIFetcher()
    
    # Fetch data (try with SSL verification first, then without if it fails)
    if not fetcher.fetch_data(verify_ssl=True):
        print("\n⚠️  Retrying without SSL verification...")
        if not fetcher.fetch_data(verify_ssl=False):
            return
    
    # Display overall summary
    fetcher.display_summary()
    
    # Display summary for specific counties
    print("\n")
    fetcher.display_county_summary("臺北市")
    
    print("\n")
    fetcher.display_county_summary("新北市")
    
    # Check for unhealthy air quality (AQI > 100)
    print("\n")
    unhealthy_stations = fetcher.get_unhealthy_stations(aqi_threshold=100)
    if unhealthy_stations:
        print("⚠️  空氣品質不良警示 (AQI > 100):")
        print("="*80)
        for station in unhealthy_stations:
            print(f"  {station['county']} - {station['sitename']}: AQI {station['aqi']} ({station['status']})")
    else:
        print("✓ 所有測站空氣品質良好 (AQI ≤ 100)")
    
    # Display detailed information for a specific station
    print("\n")
    taipei_station = fetcher.get_station_by_name("古亭")
    if taipei_station:
        fetcher.display_station(taipei_station)
    
    # Save data to file
    print("\n")
    fetcher.save_to_file("aqi_data.json")


if __name__ == "__main__":
    main()
