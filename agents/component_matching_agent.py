from .base_agent import BaseAgent
from typing import Any, Dict
from core.utils import load_component_data

class ComponentMatchingAgent(BaseAgent):
    """Matches compatible system components"""
    
    def __init__(self):
        super().__init__("ComponentMatching")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Match compatible components"""
        try:
            # Get component recommendations
            panels = input_data.get('recommended_panels', [])
            batteries = input_data.get('recommended_batteries', [])
            peak_load = input_data.get('peak_load_watts', 0)
            
            # Load inverters and controllers
            inverters_df = load_component_data('inverter')
            controllers_df = load_component_data('controller')
            
            # Create system configurations
            system_configs = self._create_system_configurations(
                panels, batteries, inverters_df, controllers_df, peak_load
            )
            
            return {
                "status": "success",
                "system_configurations": system_configs,
                "compatibility_matrix": self._create_compatibility_matrix(panels, batteries)
            }
            
        except Exception as e:
            self.logger.error(f"Component matching failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _create_system_configurations(self, panels, batteries, inverters_df, controllers_df, peak_load):
        """Create complete system configurations"""
        configurations = []
        
        # Get suitable inverters
        suitable_inverters = self._find_suitable_inverters(inverters_df, peak_load)
        
        # Get suitable controllers  
        suitable_controllers = self._find_suitable_controllers(controllers_df, panels)
        
        # Create configurations (top 5 combinations)
        for i, panel_config in enumerate(panels[:3]):
            for j, battery_config in enumerate(batteries[:3]):
                for inverter in suitable_inverters[:2]:
                    for controller in suitable_controllers[:2]:
                        
                        total_cost = (
                            panel_config.get('total_cost', 0) +
                            battery_config.get('total_cost', 0) +
                            inverter.get('price', 0) +
                            controller.get('price', 0)
                        )
                        
                        configurations.append({
                            'config_id': f"CONFIG_{i}_{j}",
                            'panel': panel_config,
                            'battery': battery_config,
                            'inverter': inverter,
                            'controller': controller,
                            'total_system_cost': total_cost,
                            'cost_per_watt': total_cost / panel_config.get('total_capacity', 1)
                        })
        
        # Sort by total cost
        configurations.sort(key=lambda x: x['total_system_cost'])
        return configurations[:10]
    
    def _find_suitable_inverters(self, inverters_df, peak_load):
        """Find suitable inverters for peak load"""
        suitable = []
        required_capacity = peak_load * 1.25  # 25% safety margin
        
        for _, inverter in inverters_df.iterrows():
            power_rating = inverter.get('power_rating', 0)
            if power_rating >= required_capacity:
                suitable.append({
                    'model': inverter.get('model', 'Unknown'),
                    'power_rating': power_rating,
                    'price': inverter.get('price', 0),
                    'efficiency': inverter.get('efficiency', 0.9),
                    'input_voltage': inverter.get('input_voltage', 12)
                })
        
        return sorted(suitable, key=lambda x: x['price'])
    
    def _find_suitable_controllers(self, controllers_df, panels):
        """Find suitable charge controllers"""
        suitable = []
        
        if not panels:
            return suitable
        
        max_panel_current = max([p.get('total_capacity', 0) / 12 for p in panels])
        
        for _, controller in controllers_df.iterrows():
            max_current = controller.get('max_current', 0)
            if max_current >= max_panel_current * 1.25:  # 25% margin
                suitable.append({
                    'model': controller.get('model', 'Unknown'),
                    'max_current': max_current,
                    'price': controller.get('price', 0),
                    'efficiency': controller.get('efficiency', 0.98),
                    'voltage': controller.get('voltage', 12)
                })
        
        return sorted(suitable, key=lambda x: x['price'])
    
    def _create_compatibility_matrix(self, panels, batteries):
        """Create component compatibility matrix"""
        matrix = {}
        
        for panel in panels[:5]:
            panel_key = panel.get('model', 'Unknown')
            matrix[panel_key] = {}
            
            for battery in batteries[:5]:
                battery_key = battery.get('model', 'Unknown')
                
                # Simple compatibility check (voltage matching)
                panel_voltage = panel.get('panel_voltage', 12)
                battery_voltage = battery.get('voltage', 12)
                
                compatible = abs(panel_voltage - battery_voltage) <= 2
                
                matrix[panel_key][battery_key] = {
                    'compatible': compatible,
                    'compatibility_score': 1.0 if compatible else 0.5
                }
        
        return matrix