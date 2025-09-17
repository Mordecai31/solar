class SolarConstants:
    # Solar calculation constants
    STANDARD_TEST_CONDITIONS = 1000  # W/m²
    CELL_TEMPERATURE_COEFFICIENT = -0.004  # per °C
    STANDARD_CELL_TEMPERATURE = 25  # °C
    AVERAGE_CELL_TEMPERATURE = 45  # °C in Nigeria
    
    # System efficiency factors
    INVERTER_EFFICIENCY = 0.90
    CHARGE_CONTROLLER_EFFICIENCY = 0.98
    BATTERY_EFFICIENCY = 0.85
    WIRING_EFFICIENCY = 0.95
    DUST_SOILING_FACTOR = 0.95
    
    # Battery constants
    BATTERY_DEPTH_OF_DISCHARGE = 0.8  # 80% DOD for lithium
    BATTERY_DAYS_AUTONOMY = 2
    
    # Nigerian specific
    AVERAGE_SUNSHINE_HOURS = 6
    GRID_ELECTRICITY_COST_PER_KWH = 45  # Naira per kWh
    CO2_PER_KWH_GRID = 0.459  # kg CO2 per kWh