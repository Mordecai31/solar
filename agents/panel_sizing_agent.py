import math
from .base_agent import BaseAgent
from core.calculations import SolarCalculations
from core.utils import load_component_data
from typing import Any, Dict

class PanelSizingAgent(BaseAgent):
    """Sizes solar panel requirements"""
    
    def __init__(self):
        super().__init__("PanelSizing")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate panel sizing requirements"""
        try:
            # Required inputs
            daily_consumption = input_data['daily_consumption_kwh']
            peak_sun_hours = input_data['peak_sun_hours']
            system_efficiency = input_data.get('system_efficiency', 0.8)
            
            # Calculate panel requirements
            required_capacity = SolarCalculations.calculate_panel_requirements(
                daily_consumption, peak_sun_hours, system_efficiency
            )
            
            # Load available panels
            # **INPUT YOUR PANEL DATA LOADING HERE**
            panels_df = load_component_data('panel')
            
            # Find suitable panels
            suitable_panels = self._find_suitable_panels(panels_df, required_capacity)
            
            return {
                "status": "success",
                "required_capacity_watts": required_capacity,
                "recommended_panels": suitable_panels,
                "system_efficiency": system_efficiency,
                "sizing_details": {
                    "daily_consumption": daily_consumption,
                    "peak_sun_hours": peak_sun_hours,
                    "derating_factor": 1 - system_efficiency
                }
            }
            
        except Exception as e:
            self.logger.error(f"Panel sizing failed: {e}")
            return {
                "status": "error", 
                "error": str(e)
            }
    
    def _find_suitable_panels(self, panels_df, required_capacity):
        """Find suitable panel configurations"""
        # **IMPLEMENT BASED ON YOUR PANEL DATA STRUCTURE**
        suitable_panels = []
        
        for _, panel in panels_df.iterrows():
            panel_power = panel.get('power_rating', 0)
            if panel_power > 0:
                num_panels = math.ceil(required_capacity / panel_power)
                total_capacity = num_panels * panel_power
                total_cost = num_panels * panel.get('price', 0)
                
                suitable_panels.append({
                    'model': panel.get('model', 'Unknown'),
                    'panel_power': panel_power,
                    'number_needed': num_panels,
                    'total_capacity': total_capacity,
                    'total_cost': total_cost,
                    'cost_per_watt': total_cost / total_capacity if total_capacity > 0 else 0
                })
        
        # Sort by cost per watt
        suitable_panels.sort(key=lambda x: x['cost_per_watt'])
        
        return suitable_panels[:10]