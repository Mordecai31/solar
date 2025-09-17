from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./solar_calculator.db"
    
    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379"
    
    # NASA POWER API
    NASA_POWER_API_BASE: str = "https://power.larc.nasa.gov/api"
    NASA_POWER_API_TIMEOUT: int = 30
    
    # File paths
    DATA_PATH: str = "data"
    RAW_DATA_PATH: str = "data/raw"
    PROCESSED_DATA_PATH: str = "data/processed"
    
    # **INPUT YOUR DATA FILE PATHS HERE**
    BATTERIES_CSV: str = "data/raw/batteries.csv"
    CONTROLLERS_CSV: str = "data/raw/controllers.csv"
    INVERTERS_CSV: str = "data/raw/inverters.csv"
    PANELS_CSV: str = "data/raw/panels.csv"
    APPLIANCES_CSV: str = "data/raw/appliances.csv"
    
    # System constants
    DEFAULT_SYSTEM_EFFICIENCY: float = 0.8
    DEFAULT_BATTERY_DOD: float = 0.8
    DEFAULT_PEAK_SUN_HOURS: float = 6.0
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 1
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/solar_calculator.log"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

