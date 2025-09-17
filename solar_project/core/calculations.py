from typing import List
from solar_project.data.schemas.user_input_schemas import Appliance

def calculate_total_daily_load_wh(appliances: List[Appliance]) -> float:
    """
    Calculates the total daily energy consumption (load) in Watt-hours.

    Args:
        appliances: A list of Appliance data models.

    Returns:
        The total energy consumption in Watt-hours per day.
    """
    total_wh = 0.0
    for appliance in appliances:
        total_wh += appliance.wattage * appliance.hours_per_day * appliance.quantity
    return total_wh
