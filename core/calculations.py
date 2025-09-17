import math
from typing import Dict, List, Tuple

class SolarCalculations:
    
    @staticmethod
    def calculate_daily_energy_consumption(appliances: List[Dict]) -> float:
        """Calculate total daily energy consumption in kWh"""
        total_consumption = 0
        
        for appliance in appliances:
            power_rating = appliance.get('power_rating', 0)  # Watts
            hours_per_day = appliance.get('hours_per_day', 0)
            quantity = appliance.get('quantity', 1)
            
            daily_consumption = (power_rating * hours_per_day * quantity) / 1000  # kWh
            total_consumption += daily_consumption
        
        return total_consumption
    
    @staticmethod
    def calculate_peak_load(appliances: List[Dict]) -> float:
        """Calculate peak load in Watts"""
        peak_load = 0
        
        for appliance in appliances:
            power_rating = appliance.get('power_rating', 0)
            quantity = appliance.get('quantity', 1)
            peak_load += power_rating * quantity
        
        return peak_load
    
    @staticmethod
    def calculate_panel_requirements(daily_consumption: float, peak_sun_hours: float, 
                                   system_efficiency: float = 0.8) -> float:
        """Calculate required panel capacity in Watts"""
        # Account for system losses
        adjusted_consumption = daily_consumption / system_efficiency
        
        # Required panel capacity
        panel_capacity = (adjusted_consumption * 1000) / peak_sun_hours  # Watts
        
        return panel_capacity
    
    @staticmethod
    def calculate_battery_requirements(daily_consumption: float, backup_days: float = 2,
                                     depth_of_discharge: float = 0.8,
                                     battery_voltage: float = 12) -> float:
        """Calculate required battery capacity in Ah"""
        # Energy storage needed
        energy_needed = daily_consumption * backup_days  # kWh
        
        # Convert to Amp-hours
        capacity_ah = (energy_needed * 1000) / (battery_voltage * depth_of_discharge)
        
        return capacity_ah
    
    @staticmethod
    def calculate_inverter_requirements(peak_load: float, safety_factor: float = 1.25) -> float:
        """Calculate required inverter capacity in Watts"""
        return peak_load * safety_factor
    
    @staticmethod
    def estimate_solar_irradiance(latitude: float, month: int) -> float:
        """Estimate solar irradiance based on location and month"""
        # **INPUT YOUR IRRADIANCE CALCULATION LOGIC HERE**
        # This is where you would use your actual irradiance data
        # or NASA POWER API
        
        # Placeholder - replace with your actual data/API call
        base_irradiance = 5.0  # kWh/m²/day
        
        # Seasonal adjustment (very simplified)
        seasonal_factor = 1 + 0.2 * math.sin((month - 6) * math.pi / 6)
        
        # Latitude adjustment (simplified)
        latitude_factor = 1 - abs(latitude - 10) * 0.01  # Nigeria is around 10°N
        
        return base_irradiance * seasonal_factor * latitude_factor
