import pytest
from solar_project.core.calculations import calculate_total_daily_load_wh
from solar_project.data.schemas.user_input_schemas import Appliance

def test_calculate_total_daily_load_wh_empty_list():
    """Tests that the calculation returns 0 for an empty list of appliances."""
    assert calculate_total_daily_load_wh([]) == 0.0

def test_calculate_total_daily_load_wh_single_appliance():
    """Tests the calculation for a single appliance."""
    appliances = [
        Appliance(name="TV", wattage=150, hours_per_day=5, quantity=1)
    ]
    # Expected: 150 * 5 * 1 = 750
    assert calculate_total_daily_load_wh(appliances) == 750.0

def test_calculate_total_daily_load_wh_multiple_appliances():
    """Tests the calculation for a list of multiple appliances."""
    appliances = [
        Appliance(name="Fridge", wattage=200, hours_per_day=24, quantity=1), # 4800 Wh
        Appliance(name="Fan", wattage=75, hours_per_day=12, quantity=2),    # 1800 Wh
        Appliance(name="Lights", wattage=10, hours_per_day=6, quantity=5), # 300 Wh
    ]
    # Expected: 4800 + 1800 + 300 = 6900
    assert calculate_total_daily_load_wh(appliances) == 6900.0
