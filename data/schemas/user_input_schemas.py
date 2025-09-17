from pydantic import BaseModel, Field
from typing import List, Optional

class ApplianceInput(BaseModel):
    appliance: str = Field(..., description="Appliance name")
    power_rating: float = Field(..., gt=0, description="Power rating in Watts")
    hours_per_day: float = Field(..., ge=0, le=24, description="Usage hours per day")
    quantity: int = Field(1, ge=1, description="Number of appliances")

class UserInput(BaseModel):
    location: str = Field(..., description="User location")
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    budget: float = Field(..., gt=0, description="Budget in Naira")
    appliances: List[ApplianceInput]
    backup_hours: float = Field(4, ge=1, le=72, description="Required backup hours")
    system_expansion: bool = Field(False, description="Plan for future expansion")
    priority: str = Field("balanced", regex="^(cost|reliability|efficiency|balanced)$")
