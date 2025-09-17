from .base_agent import BaseAgent
from typing import Any, Dict

class CostOptimizerAgent(BaseAgent):
    """Optimizes system cost within budget constraints"""
    
    def __init__(self):
        super().__init__("CostOptimizer")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize system cost"""
        try:
            budget = input_data.get('budget', 0)
            system_configs = input_data.get('system_configurations', [])
            priority = input_data.get('priority', 'balanced')
            
            # Filter configurations within budget
            affordable_configs = [
                config for config in system_configs 
                if config.get('total_system_cost', 0) <= budget
            ]
            
            if not affordable_configs:
                # Find closest to budget
                affordable_configs = sorted(
                    system_configs, 
                    key=lambda x: abs(x.get('total_system_cost', 0) - budget)
                )[:3]
            
            # Optimize based on priority
            optimized_configs = self._optimize_by_priority(affordable_configs, priority)
            
            return {
                "status": "success",
                "budget": budget,
                "affordable_configurations": optimized_configs,
                "savings_analysis": self._calculate_savings_analysis(optimized_configs),
                "financing_options": self._suggest_financing_options(budget, optimized_configs)
            }
            
        except Exception as e:
            self.logger.error(f"Cost optimization failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _optimize_by_priority(self, configs, priority):
        """Optimize configurations by priority"""
        if priority == 'cost':
            return sorted(configs, key=lambda x: x.get('total_system_cost', 0))
        elif priority == 'reliability':
            return sorted(configs, key=lambda x: -x.get('reliability_score', 0))
        elif priority == 'efficiency':
            return sorted(configs, key=lambda x: -x.get('efficiency_score', 0))
        else:  # balanced
            return sorted(configs, key=lambda x: x.get('balanced_score', 0))
    
    def _calculate_savings_analysis(self, configs):
        """Calculate potential savings for each configuration"""
        analysis = []
        
        for config in configs[:3]:
            panel_capacity = config.get('panel', {}).get('total_capacity', 0)
            monthly_generation = panel_capacity * 6 * 30 / 1000  # kWh/month (rough estimate)
            monthly_savings = monthly_generation * 45  # ₦45 per kWh
            
            system_cost = config.get('total_system_cost', 0)
            payback_years = system_cost / (monthly_savings * 12) if monthly_savings > 0 else float('inf')
            
            analysis.append({
                'config_id': config.get('config_id'),
                'monthly_savings': monthly_savings,
                'annual_savings': monthly_savings * 12,
                'payback_period_years': round(payback_years, 1),
                'roi_percentage': round((monthly_savings * 12) / system_cost * 100, 1) if system_cost > 0 else 0
            })
        
        return analysis
    
    def _suggest_financing_options(self, budget, configs):
        """Suggest financing options if needed"""
        options = []
        
        if not configs:
            return options
        
        min_cost = min([c.get('total_system_cost', 0) for c in configs])
        
        if min_cost > budget:
            # Suggest financing options
            options.append({
                'option': 'installment_payment',
                'description': 'Pay in installments over 6-12 months',
                'monthly_payment': min_cost / 12,
                'total_cost': min_cost * 1.05  # 5% financing cost
            })
            
            options.append({
                'option': 'phased_installation',
                'description': 'Install system in phases',
                'phase_1_cost': budget,
                'remaining_cost': min_cost - budget
            })
        
        return options