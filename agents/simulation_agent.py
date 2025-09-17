from .base_agent import BaseAgent
import numpy as np
from datetime import datetime, timedelta
from typing import Any, Dict

class SimulationAgent(BaseAgent):
    """Simulates system performance over time"""
    
    def __init__(self):
        super().__init__("SystemSimulation")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run system performance simulation"""
        try:
            # Get system configuration
            system_config = input_data.get('selected_configuration', {})
            load_profile = input_data.get('load_profile', {})
            irradiance_data = input_data.get('irradiance_data', {})
            
            # Run simulation
            simulation_results = self._run_annual_simulation(
                system_config, load_profile, irradiance_data
            )
            
            return {
                "status": "success",
                "simulation_results": simulation_results,
                "performance_metrics": self._calculate_performance_metrics(simulation_results),
                "recommendations": self._generate_performance_recommendations(simulation_results)
            }
            
        except Exception as e:
            self.logger.error(f"System simulation failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _run_annual_simulation(self, system_config, load_profile, irradiance_data):
        """Run 365-day system simulation"""
        results = {
            'daily_results': [],
            'monthly_summary': {},
            'annual_totals': {}
        }
        
        # System specifications
        panel_capacity = system_config.get('panel', {}).get('total_capacity', 0)
        battery_capacity = system_config.get('battery', {}).get('total_capacity_ah', 0)
        inverter_efficiency = system_config.get('inverter', {}).get('efficiency', 0.9)
        
        # Daily simulation
        battery_soc = 0.8  # Start at 80% SOC
        
        for day in range(365):
            month = (day // 30) + 1
            if month > 12:
                month = 12
            
            # Get daily irradiance (use monthly average)
            daily_irradiance = irradiance_data.get('daily_irradiance_kwh_m2', 5.0)
            
            # Solar generation
            daily_generation = (panel_capacity * daily_irradiance * 0.8) / 1000  # kWh
            
            # Load consumption
            daily_consumption = load_profile.get('total_energy_kwh', 5.0)
            
            # Battery simulation
            excess_energy = daily_generation - daily_consumption
            
            if excess_energy > 0:
                # Charge battery
                battery_soc = min(1.0, battery_soc + (excess_energy / (battery_capacity * 12 / 1000)))
            else:
                # Discharge battery
                battery_soc = max(0.2, battery_soc + (excess_energy / (battery_capacity * 12 / 1000)))
            
            grid_import = max(0, -excess_energy) if battery_soc <= 0.2 else 0
            
            results['daily_results'].append({
                'day': day + 1,
                'generation_kwh': daily_generation,
                'consumption_kwh': daily_consumption,
                'battery_soc': battery_soc,
                'grid_import_kwh': grid_import,
                'excess_energy_kwh': max(0, excess_energy)
            })
        
        # Calculate monthly summaries
        for month in range(1, 13):
            month_days = [r for r in results['daily_results'] 
                         if ((r['day'] - 1) // 30) + 1 == month]
            
            results['monthly_summary'][month] = {
                'generation_kwh': sum(d['generation_kwh'] for d in month_days),
                'consumption_kwh': sum(d['consumption_kwh'] for d in month_days),
                'grid_import_kwh': sum(d['grid_import_kwh'] for d in month_days),
                'self_consumption_ratio': self._calculate_self_consumption_ratio(month_days)
            }
        
        # Annual totals
        results['annual_totals'] = {
            'generation_kwh': sum(d['generation_kwh'] for d in results['daily_results']),
            'consumption_kwh': sum(d['consumption_kwh'] for d in results['daily_results']),
            'grid_import_kwh': sum(d['grid_import_kwh'] for d in results['daily_results']),
            'self_sufficiency_ratio': 1 - (sum(d['grid_import_kwh'] for d in results['daily_results']) / 
                                          sum(d['consumption_kwh'] for d in results['daily_results']))
        }
        
        return results
    
    def _calculate_self_consumption_ratio(self, daily_data):
        """Calculate self-consumption ratio for a period"""
        total_generation = sum(d['generation_kwh'] for d in daily_data)
        total_consumption = sum(d['consumption_kwh'] for d in daily_data)
        
        if total_generation == 0:
            return 0
        
        self_consumed = min(total_generation, total_consumption)
        return self_consumed / total_generation
    
    def _calculate_performance_metrics(self, simulation_results):
        """Calculate key performance metrics"""
        annual = simulation_results['annual_totals']
        
        return {
            'system_efficiency': round(annual['generation_kwh'] / (annual['generation_kwh'] + annual['grid_import_kwh']), 3),
            'self_sufficiency_ratio': round(annual['self_sufficiency_ratio'], 3),
            'capacity_factor': round(annual['generation_kwh'] / (8760 * 5), 3),  # Assuming 5kW system
            'performance_ratio': round(annual['generation_kwh'] / (5 * 1825), 3),  # 5 hours * 365 days
            'grid_independence_days': len([d for d in simulation_results['daily_results'] if d['grid_import_kwh'] == 0])
        }
    
    def _generate_performance_recommendations(self, simulation_results):
        """Generate performance-based recommendations"""
        recommendations = []
        
        annual = simulation_results['annual_totals']
        self_sufficiency = annual['self_sufficiency_ratio']
        
        if self_sufficiency < 0.7:
            recommendations.append({
                'category': 'system_sizing',
                'message': 'Consider increasing battery or panel capacity for better self-sufficiency',
                'priority': 'high'
            })
        
        if annual['grid_import_kwh'] > annual['consumption_kwh'] * 0.5:
            recommendations.append({
                'category': 'energy_management',
                'message': 'Optimize energy usage patterns to maximize solar utilization',
                'priority': 'medium'
            })
        
        # Check seasonal performance
        monthly = simulation_results['monthly_summary']
        worst_month = min(monthly.keys(), key=lambda m: monthly[m]['self_consumption_ratio'])
        
        if monthly[worst_month]['self_consumption_ratio'] < 0.5:
            recommendations.append({
                'category': 'seasonal_optimization',
                'message': f'Consider energy storage optimization for month {worst_month}',
                'priority': 'medium'
            })
        
        return recommendations