import pandas as pd
import json
from typing import Dict, Any, Optional
import os

def load_component_data(component_type: str, data_path: str = "data/raw/") -> pd.DataFrame:
    """Load component data from CSV files"""
    # **INPUT YOUR CSV FILE PATHS HERE**
    file_map = {
        'battery': f"{data_path}batteries.csv",
        'controller': f"{data_path}controllers.csv", 
        'inverter': f"{data_path}inverters.csv",
        'panel': f"{data_path}panels.csv"
    }
    
    if component_type not in file_map:
        raise ValueError(f"Unknown component type: {component_type}")
    
    file_path = file_map[component_type]
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Component data file not found: {file_path}")
    
    return pd.read_csv(file_path)

def load_appliance_data(data_path: str = "data/raw/appliances.csv") -> pd.DataFrame:
    """Load appliance data"""
    # **INPUT YOUR APPLIANCE CSV FILE PATH HERE**
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Appliance data file not found: {data_path}")
    
    return pd.read_csv(data_path)

def save_results(results: Dict[str, Any], filename: str, output_dir: str = "outputs/"):
    """Save calculation results"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def format_currency(amount: float, currency: str = "₦") -> str:
    """Format currency for display"""
    return f"{currency}{amount:,.2f}"

def calculate_payback_period(system_cost: float, monthly_savings: float) -> float:
    """Calculate payback period in years"""
    if monthly_savings <= 0:
        return float('inf')
    
    annual_savings = monthly_savings * 12
    return system_cost / annual_savings