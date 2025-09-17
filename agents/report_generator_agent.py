from .base_agent import BaseAgent
from datetime import datetime
import json 
from typing import Any, Dict

class ReportGeneratorAgent(BaseAgent):
    """Generates comprehensive system reports"""
    
    def __init__(self):
        super().__init__("ReportGenerator")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive system report"""
        try:
            # Compile all data
            report = self._compile_comprehensive_report(input_data)
            
            # Generate different report formats
            executive_summary = self._generate_executive_summary(report)
            technical_details = self._generate_technical_details(report)
            financial_analysis = self._generate_financial_analysis(report)
            
            return {
                "status": "success",
                "report_generated": datetime.now().isoformat(),
                "executive_summary": executive_summary,
                "technical_details": technical_details,
                "financial_analysis": financial_analysis,
                "full_report": report
            }
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _compile_comprehensive_report(self, input_data):
        """Compile all analysis results into comprehensive report"""
        return {
            'project_info': {
                'location': input_data.get('location', 'Unknown'),
                'analysis_date': datetime.now().strftime('%Y-%m-%d'),
                'budget': input_data.get('budget', 0)
            },
            'load_analysis': input_data.get('load_analysis', {}),
            'system_design': input_data.get('selected_configuration', {}),
            'performance_simulation': input_data.get('simulation_results', {}),
            'financial_projections': input_data.get('savings_analysis', {}),
            'recommendations': input_data.get('recommendations', [])
        }
    
    def _generate_executive_summary(self, report):
        """Generate executive summary"""
        system_cost = report.get('system_design', {}).get('total_system_cost', 0)
        daily_consumption = report.get('load_analysis', {}).get('daily_consumption_kwh', 0)
        annual_savings = report.get('financial_projections', {}).get('annual_savings', 0)
        
        return {
            'recommended_system_cost': system_cost,
            'daily_energy_needs': daily_consumption,
            'projected_annual_savings': annual_savings,
            'payback_period': report.get('financial_projections', {}).get('payback_period_years', 0),
            'key_benefits': [
                f'Reduce electricity costs by ₦{annual_savings:,.0f} annually',
                f'Meet {daily_consumption:.1f} kWh daily energy needs',
                'Reduce carbon footprint',
                'Energy independence from grid instability'
            ]
        }
    
    def _generate_technical_details(self, report):
        """Generate technical specifications"""
        system_design = report.get('system_design', {})
        
        return {
            'solar_panels': system_design.get('panel', {}),
            'battery_system': system_design.get('battery', {}),
            'inverter': system_design.get('inverter', {}),
            'charge_controller': system_design.get('controller', {}),
            'system_specifications': {
                'total_panel_capacity': system_design.get('panel', {}).get('total_capacity', 0),
                'total_battery_capacity': system_design.get('battery', {}).get('total_capacity_ah', 0),
                'inverter_capacity': system_design.get('inverter', {}).get('power_rating', 0),
                'expected_daily_generation': report.get('performance_simulation', {}).get('annual_totals', {}).get('generation_kwh', 0) / 365
            }
        }
    
    def _generate_financial_analysis(self, report):
        """Generate detailed financial analysis"""
        system_cost = report.get('system_design', {}).get('total_system_cost', 0)
        annual_savings = report.get('financial_projections', {}).get('annual_savings', 0)
        
        # 25-year projection
        projection_years = 25
        cumulative_savings = []
        
        for year in range(1, projection_years + 1):
            # Account for electricity price inflation (5% annually)
            inflation_factor = 1.05 ** year
            yearly_savings = annual_savings * inflation_factor
            
            if year == 1:
                cumulative = yearly_savings - system_cost
            else:
                cumulative = cumulative_savings[-1] + yearly_savings
            
            cumulative_savings.append(cumulative)
        
        return {
            'initial_investment': system_cost,
            'annual_savings_year_1': annual_savings,
            'payback_period_years': system_cost / annual_savings if annual_savings > 0 else float('inf'),
            'net_savings_25_years': cumulative_savings[-1] if cumulative_savings else 0,
            'roi_percentage': (cumulative_savings[-1] / system_cost * 100) if system_cost > 0 and cumulative_savings else 0,
            'break_even_year': next((i+1 for i, val in enumerate(cumulative_savings) if val > 0), None),
            'financing_options': report.get('financing_options', [])
        }