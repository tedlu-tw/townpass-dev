#!/usr/bin/env python3
"""
YouBike Data Fetcher
Fetches real-time YouBike station data from Taipei City API
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class YouBikeFetcher:
    """Fetches and processes YouBike station data"""
    
    API_URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    
    def __init__(self):
        self.data: Optional[List[Dict]] = None
    
    def fetch_data(self, timeout: int = 10) -> bool:
        """
        Fetch data from YouBike API
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Fetching data from {self.API_URL}...")
            response = requests.get(self.API_URL, timeout=timeout)
            response.raise_for_status()
            
            self.data = response.json()
            print(f"✓ Successfully fetched {len(self.data)} stations")
            return True
            
        except requests.exceptions.Timeout:
            print(f"✗ Error: Request timed out after {timeout} seconds")
            return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching data: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON: {e}")
            return False
    
    def get_station_by_sno(self, sno: str) -> Optional[Dict]:
        """Get station data by station number"""
        if not self.data:
            return None
        
        for station in self.data:
            if station.get('sno') == sno:
                return station
        return None
    
    def get_stations_by_area(self, area: str) -> List[Dict]:
        """Get all stations in a specific area"""
        if not self.data:
            return []
        
        return [s for s in self.data if s.get('sarea') == area or s.get('sareaen') == area]
    
    def get_available_stations(self, min_bikes: int = 1) -> List[Dict]:
        """Get stations with available bikes"""
        if not self.data:
            return []
        
        return [s for s in self.data if s.get('available_rent_bikes', 0) >= min_bikes]
    
    def display_station(self, station: Dict):
        """Display formatted station information"""
        print("\n" + "="*60)
        print(f"Station: {station.get('sna', 'N/A')}")
        print(f"English: {station.get('snaen', 'N/A')}")
        print(f"Area: {station.get('sarea', 'N/A')} ({station.get('sareaen', 'N/A')})")
        print(f"Address: {station.get('ar', 'N/A')}")
        print(f"Total Capacity: {station.get('Quantity', 0)}")
        print(f"Available Bikes: {station.get('available_rent_bikes', 0)}")
        print(f"Available Spaces: {station.get('available_return_bikes', 0)}")
        print(f"Location: ({station.get('latitude', 'N/A')}, {station.get('longitude', 'N/A')})")
        print(f"Last Update: {station.get('updateTime', 'N/A')}")
        print(f"Active: {'Yes' if station.get('act') == '1' else 'No'}")
        print("="*60)
    
    def display_summary(self):
        """Display summary statistics"""
        if not self.data:
            print("No data available")
            return
        
        total_stations = len(self.data)
        total_bikes = sum(s.get('available_rent_bikes', 0) for s in self.data)
        total_spaces = sum(s.get('available_return_bikes', 0) for s in self.data)
        active_stations = sum(1 for s in self.data if s.get('act') == '1')
        
        print("\n" + "="*60)
        print("YouBike System Summary")
        print("="*60)
        print(f"Total Stations: {total_stations}")
        print(f"Active Stations: {active_stations}")
        print(f"Total Available Bikes: {total_bikes}")
        print(f"Total Available Spaces: {total_spaces}")
        print("="*60)
    
    def save_to_file(self, filename: str = "youbike_data.json", output_dir: str = "data"):
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
    fetcher = YouBikeFetcher()
    
    # Fetch data
    if not fetcher.fetch_data():
        return
    
    # Display summary
    fetcher.display_summary()
    
    # Example: Find stations in Daan District
    print("\n\nStations in Daan District (大安區):")
    daan_stations = fetcher.get_stations_by_area("大安區")
    print(f"Found {len(daan_stations)} stations")
    
    # Display first station as example
    if daan_stations:
        print("\nExample station:")
        fetcher.display_station(daan_stations[0])
    
    # Example: Find stations with at least 5 bikes available
    print("\n\nStations with 5+ bikes available:")
    available_stations = fetcher.get_available_stations(min_bikes=5)
    print(f"Found {len(available_stations)} stations")
    
    # Save data to file
    print("\n")
    fetcher.save_to_file("youbike_data.json")


if __name__ == "__main__":
    main()
