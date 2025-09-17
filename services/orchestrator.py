from typing import Dict, Any, List
import logging
from agents.input_validation_agent import InputValidationAgent
from agents.load_calculator_agent import LoadCalculatorAgent
from agents.irradiance_agent import IrradianceAgent
from agents.panel_sizing_agent import PanelSizingAgent
from agents.battery_sizing_agent import BatterySizingAgent
from agents.component_matching_agent import ComponentMatchingAgent
from agents.cost_optimizer_agent import CostOptimizerAgent
from agents.simulation_agent import SimulationAgent
from agents.report_generator_agent import ReportGeneratorAgent

logger = logging.getLogger(__name__)

class SolarSystemOrchestrator:
    """Main orchestrator for solar system calculation workflow"""
    
    def __init__(self):
        self.agents = {
            'input_validator': InputValidationAgent(),
            'load_calculator': LoadCalculatorAgent(),
            'irradiance_agent': IrradianceAgent(),
            'panel_sizing': PanelSizingAgent(),
            'battery_sizing': BatterySizingAgent(),
            'component_matching': ComponentMatchingAgent(),
            'cost_optimizer': CostOptimizerAgent(),
            'simulation': SimulationAgent(),
            'report_generator': ReportGeneratorAgent()
        }
    
    def calculate_solar_system(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Main calculation workflow"""
        try:
            logger.info("Starting solar system calculation")
            workflow_data = {}
            
            # Step 1: Validate Input
            logger.info("Step 1: Validating input")
            validation_result = self.agents['input_validator'].process(user_input)
            if validation_result['status'] != 'success':
                return validation_result
            
            workflow_data.update(validation_result['validated_data'])
            
            # Step 2: Calculate Load Requirements
            logger.info("Step 2: Calculating load requirements")
            load_result = self.agents['load_calculator'].process(workflow_data)
            if load_result['status'] != 'success':
                return load_result
            
            workflow_data.update(load_result)
            
            # Step 3: Get Irradiance Data
            logger.info("Step 3: Getting irradiance data")
            irradiance_result = self.agents['irradiance_agent'].process(workflow_data)
            workflow_data.update(irradiance_result)
            
            # Step 4: Size Solar Panels
            logger.info("Step 4: Sizing solar panels")
            panel_result = self.agents['panel_sizing'].process(workflow_data)
            if panel_result['status'] != 'success':
                return panel_result
            
            workflow_data.update(panel_result)
            
            # Step 5: Size Battery System
            logger.info("Step 5: Sizing battery system")
            battery_result = self.agents['battery_sizing'].process(workflow_data)
            if battery_result['status'] != 'success':
                return battery_result
            
            workflow_data.update(battery_result)
            
            # Step 6: Match Compatible Components
            logger.info("Step 6: Matching compatible components")
            matching_result = self.agents['component_matching'].process(workflow_data)
            if matching_result['status'] != 'success':
                return matching_result
            
            workflow_data.update(matching_result)
            
            # Step 7: Optimize Cost
            logger.info("Step 7: Optimizing cost")
            optimization_result = self.agents['cost_optimizer'].process(workflow_data)
            if optimization_result['status'] != 'success':
                return optimization_result
            
            workflow_data.update(optimization_result)
            
            # Step 8: Run System Simulation
            logger.info("Step 8: Running system simulation")
            if workflow_data.get('affordable_configurations'):
                # Use best configuration for simulation
                workflow_data['selected_configuration'] = workflow_data['affordable_configurations'][0]
                simulation_result = self.agents['simulation'].process(workflow_data)
                workflow_data.update(simulation_result)
            
            # Step 9: Generate Report
            logger.info("Step 9: Generating report")
            report_result = self.agents['report_generator'].process(workflow_data)
            
            logger.info("Solar system calculation completed successfully")
            return report_result
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'message': 'Solar system calculation failed'
            }