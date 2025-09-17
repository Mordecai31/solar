from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ComponentType(str, Enum):
    BATTERY = "battery"
    CONTROLLER = "controller"  
    INVERTER = "inverter"
    PANEL = "panel"

class BatterySchema(BaseModel):
    model: str = Field(..., description="Battery model name")
    capacity_ah: float = Field(..., gt=0, description="Battery capacity in Ah")
    voltage: float = Field(..., gt=0, description="Battery voltage")
    price: float = Field(..., gt=0, description="Price in Naira")
    brand: Optional[str] = None
    warranty_years: Optional[int] = None
    
class ControllerSchema(BaseModel):
    model: str = Field(..., description="Controller model name")
    max_current: float = Field(..., gt=0, description="Maximum current in Amps")
    voltage: float = Field(..., gt=0, description="System voltage")
    price: float = Field(..., gt=0, description="Price in Naira")
    efficiency: Optional[float] = Field(None, ge=0.8, le=1.0)
    
class InverterSchema(BaseModel):
    model: str = Field(..., description="Inverter model name")
    power_rating: float = Field(..., gt=0, description="Power rating in Watts")
    input_voltage: float = Field(..., gt=0, description="Input voltage")
    price: float = Field(..., gt=0, description="Price in Naira")
    efficiency: Optional[float] = Field(None, ge=0.8, le=1.0)
    
class PanelSchema(BaseModel):
    model: str = Field(..., description="Panel model name")
    power_rating: float = Field(..., gt=0, description="Power rating in Watts")
    voltage: float = Field(..., gt=0, description="Panel voltage")
    price: float = Field(..., gt=0, description="Price in Naira")
    efficiency: Optional[float] = Field(None, ge=0.15, le=0.25)