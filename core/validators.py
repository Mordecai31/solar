import pandas as pd
from typing import Dict, Any, List

from core.exceptions import ValidationError

def validate_user_input(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate user input data"""
    errors = []
    
    # Required fields
    required_fields = ['location', 'budget', 'appliances']
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Budget validation
    if 'budget' in user_data:
        try:
            budget = float(user_data['budget'])
            if budget <= 0:
                errors.append("Budget must be greater than 0")
        except (ValueError, TypeError):
            errors.append("Budget must be a valid number")
    
    # Appliances validation
    if 'appliances' in user_data:
        if not isinstance(user_data['appliances'], list):
            errors.append("Appliances must be a list")
        else:
            for i, appliance in enumerate(user_data['appliances']):
                if not isinstance(appliance, dict):
                    errors.append(f"Appliance {i+1} must be a dictionary")
                    continue
                
                required_app_fields = ['appliance', 'power_rating', 'hours_per_day']
                for field in required_app_fields:
                    if field not in appliance:
                        errors.append(f"Appliance {i+1} missing field: {field}")
    
    if errors:
        raise ValidationError(f"Validation errors: {', '.join(errors)}")
    
    return user_data

def validate_component_data(df: pd.DataFrame, component_type: str) -> pd.DataFrame:
    """Validate component DataFrame"""
    required_columns = {
        'battery': ['model', 'capacity_ah', 'voltage', 'price'],
        'controller': ['model', 'max_current', 'voltage', 'price'],
        'inverter': ['model', 'power_rating', 'input_voltage', 'price'],
        'panel': ['model', 'power_rating', 'voltage', 'price']
    }
    
    if component_type not in required_columns:
        raise ValidationError(f"Unknown component type: {component_type}")
    
    missing_columns = set(required_columns[component_type]) - set(df.columns)
    if missing_columns:
        raise ValidationError(f"Missing columns for {component_type}: {missing_columns}")
    
    # Remove rows with missing critical data
    df_clean = df.dropna(subset=required_columns[component_type])
    
    # Validate numeric columns
    numeric_columns = [col for col in required_columns[component_type] if col != 'model']
    for col in numeric_columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        df_clean = df_clean[df_clean[col] > 0]
    
    return df_clean