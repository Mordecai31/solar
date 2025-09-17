from .base_agent import BaseAgent
from core.calculations import SolarCalculations
from typing import Any, Dict, List

class LoadCalculatorAgent(BaseAgent):
    """Calculates energy load requirements"""
    
    def __init__(self):
        super().__init__("LoadCalculator")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate energy load requirements"""
        try:
            self.validate_input(input_data, ['appliances'])
            
            appliances = input_data['appliances']
            
            # Calculate energy requirements
            daily_consumption = SolarCalculations.calculate_daily_energy_consumption(appliances)
            peak_load = SolarCalculations.calculate_peak_load(appliances)
            
            # Calculate backup requirements
            backup_hours = input_data.get('backup_hours', 4)
            backup_energy = (peak_load * backup_hours) / 1000  # kWh
            
            results = {
                "status": "success",
                "daily_consumption_kwh": daily_consumption,
                "peak_load_watts": peak_load,
                "backup_energy_kwh": backup_energy,
                "load_profile": self._create_load_profile(appliances)
            }
            
            self.logger.info(f"Load calculation complete: {daily_consumption:.2f} kWh/day")
            return results
            
        except Exception as e:
            self.logger.error(f"Load calculation failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _create_load_profile(self, appliances: List[Dict]) -> Dict[str, Any]:
        """Create detailed load profile"""
        profile = {
            "total_appliances": len(appliances),
            "appliance_breakdown": [],
            "load_categories": {"lighting": 0, "cooling": 0, "electronics": 0, "other": 0}
        }
        
        for appliance in appliances:
            power = appliance.get('power_rating', 0)
            hours = appliance.get('hours_per_day', 0)
            qty = appliance.get('quantity', 1)
            
            daily_energy = (power * hours * qty) / 1000
            
            profile["appliance_breakdown"].append({
                "name": appliance.get('appliance', 'Unknown'),
                "power_watts": power * qty,
                "hours_per_day": hours,
                "daily_energy_kwh": daily_energy
            })
            
            # Categorize (basic categorization)
            appliance_name = appliance.get('appliance', '').lower()
            if any(word in appliance_name for word in ['light', 'bulb', 'lamp']):
                profile["load_categories"]["lighting"] += daily_energy
            elif any(word in appliance_name for word in ['fan', 'air', 'cool']):
                profile["load_categories"]["cooling"] += daily_energy
            elif any(word in appliance_name for word in ['tv', 'laptop', 'phone', 'computer']):
                profile["load_categories"]["electronics"] += daily_energy
            else:
                profile["load_categories"]["other"] += daily_energy
        
        return profile
