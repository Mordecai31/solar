from .base_agent import BaseAgent
from core.calculations import SolarCalculations
import requests
from datetime import datetime
from typing import Any, Dict

class IrradianceAgent(BaseAgent):
    """Handles solar irradiance calculations and data"""
    
    def __init__(self):
        super().__init__("IrradianceAgent")
        self.nasa_api_base = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get solar irradiance data for location"""
        try:
            latitude = input_data.get('latitude')
            longitude = input_data.get('longitude')
            location = input_data.get('location', 'Unknown')
            
            # Try to get real-time data first
            if latitude and longitude:
                irradiance_data = self._get_nasa_irradiance(latitude, longitude)
            else:
                # **INPUT YOUR LOCATION-TO-COORDINATES MAPPING HERE**
                # Use your stored data or coordinate lookup
                irradiance_data = self._get_stored_irradiance(location)
            
            return {
                "status": "success",
                "location": location,
                "latitude": latitude,
                "longitude": longitude,
                "daily_irradiance_kwh_m2": irradiance_data.get('daily_average', 5.0),
                "peak_sun_hours": irradiance_data.get('peak_sun_hours', 6.0),
                "monthly_data": irradiance_data.get('monthly_data', {}),
                "data_source": irradiance_data.get('source', 'estimated')
            }
            
        except Exception as e:
            self.logger.error(f"Irradiance calculation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "daily_irradiance_kwh_m2": 5.0,  # Fallback value
                "peak_sun_hours": 6.0
            }
    
    def _get_nasa_irradiance(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get irradiance from NASA POWER API"""
        # **INPUT YOUR NASA API IMPLEMENTATION HERE**
        try:
            params = {
                'parameters': 'ALLSKY_SFC_SW_DWN',
                'community': 'SB',
                'longitude': lon,
                'latitude': lat,
                'start': '20230101',
                'end': '20231231',
                'format': 'JSON'
            }
            
            response = requests.get(self.nasa_api_base, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            # Process NASA data here
            # This is a placeholder - implement based on actual API response
            
            return {
                'daily_average': 5.2,
                'peak_sun_hours': 6.2,
                'source': 'nasa_power_api',
                'monthly_data': {}  # Process monthly data from API
            }
            
        except Exception as e:
            self.logger.warning(f"NASA API failed: {e}, using fallback")
            return self._get_fallback_irradiance(lat)
    
    def _get_stored_irradiance(self, location: str) -> Dict[str, Any]:
        """Get irradiance from stored data"""
        # **INPUT YOUR STORED IRRADIANCE DATA LOADING HERE**
        # Load from your irradiance_monthly.csv file
        
        # Placeholder implementation
        location_data = {
            'lagos': {'daily_average': 4.8, 'peak_sun_hours': 5.8},
            'abuja': {'daily_average': 5.2, 'peak_sun_hours': 6.2},
            'kano': {'daily_average': 5.8, 'peak_sun_hours': 6.8}
        }
        
        location_key = location.lower()
        data = location_data.get(location_key, {'daily_average': 5.0, 'peak_sun_hours': 6.0})
        data['source'] = 'stored_data'
        
        return data
    
    def _get_fallback_irradiance(self, lat: float) -> Dict[str, Any]:
        """Fallback irradiance estimation"""
        # Simple latitude-based estimation for Nigeria
        base_irradiance = 5.0
        if lat > 12:  # Northern Nigeria
            base_irradiance = 5.8
        elif lat > 8:  # Middle Belt
            base_irradiance = 5.2
        else:  # Southern Nigeria
            base_irradiance = 4.8
        
        return {
            'daily_average': base_irradiance,
            'peak_sun_hours': base_irradiance * 1.2,
            'source': 'estimated'
        }