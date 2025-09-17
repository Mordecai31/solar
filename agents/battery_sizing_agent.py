from typing import Any, Dict
from .base_agent import BaseAgent
from core.calculations import SolarCalculations
from core.utils import load_component_data
import math

class BatterySizingAgent(BaseAgent):
    """Sizes battery system requirements"""
    
    def __init__(self):
        super().__init__("BatterySizing")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate battery sizing requirements"""
        try:
            # Required inputs
            daily_consumption = input_data['daily_consumption_kwh']
            backup_hours = input_data.get('backup_hours', 24)
            system_voltage = input_data.get('system_voltage', 12)
            
            # Calculate battery requirements
            required_capacity_ah = SolarCalculations.calculate_battery_requirements(
                daily_consumption, backup_hours/24, system_voltage=system_voltage
            )
            
            # Load available batteries
            # **INPUT YOUR BATTERY DATA LOADING HERE**
            batteries_df = load_component_data('battery')
            
            # Find suitable batteries
            suitable_batteries = self._find_suitable_batteries(
                batteries_df, required_capacity_ah, system_voltage
            )
            
            return {
                "status": "success",
                "required_capacity_ah": required_capacity_ah,
                "system_voltage": system_voltage,
                "backup_hours": backup_hours,
                "recommended_batteries": suitable_batteries,
                "sizing_details": {
                    "daily_consumption": daily_consumption,
                    "backup_energy_kwh": daily_consumption * (backup_hours / 24),
                    "depth_of_discharge": 0.8
                }
            }
            
        except Exception as e:
            self.logger.error(f"Battery sizing failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _find_suitable_batteries(self, batteries_df, required_capacity_ah, system_voltage):
        """Find suitable battery configurations"""
        # **IMPLEMENT BASED ON YOUR BATTERY DATA STRUCTURE**
        suitable_batteries = []
        
        for _, battery in batteries_df.iterrows():
            battery_capacity = battery.get('capacity_ah', 0)
            battery_voltage = battery.get('voltage', 12)
            
            if battery_capacity > 0:
                # Calculate number of batteries needed
                if battery_voltage == system_voltage:
                    num_batteries = math.ceil(required_capacity_ah / battery_capacity)
                    total_capacity = num_batteries * battery_capacity
                    total_cost = num_batteries * battery.get('price', 0)
                    
                    suitable_batteries.append({
                        'model': battery.get('model', 'Unknown'),
                        'battery_capacity_ah': battery_capacity,
                        'voltage': battery_voltage,
                        'number_needed': num_batteries,
                        'total_capacity_ah': total_capacity,
                        'total_cost': total_cost,
                        'cost_per_ah': total_cost / total_capacity if total_capacity > 0 else 0
                    })
        
        # Sort by cost per Ah
        suitable_batteries.sort(key=lambda x: x['cost_per_ah'])
        
        return suitable_batteries[:10]  # Return top 10 options
