from pydantic import BaseModel, Field
from typing import List, Optional

class Appliance(BaseModel):
    """
    Represents a single appliance in the user's household.
    """
    name: str = Field(..., description="Name of the appliance (e.g., 'Refrigerator').")
    wattage: float = Field(..., gt=0, description="Power consumption in watts.")
    hours_per_day: float = Field(..., ge=0, le=24, description="Average hours the appliance is used per day.")
    quantity: int = Field(1, gt=0, description="Number of this type of appliance.")

class Location(BaseModel):
    """
    Represents the user's geographical location.
    """
    state: str = Field(..., min_length=1, description="The Nigerian state for which the solar recommendation is being made.")
    # We can add more specific location data later, like city or coordinates.

class UserInput(BaseModel):
    """
    Represents the complete set of inputs provided by the user.
    """
    budget: float = Field(..., gt=0, description="The user's total budget for the solar installation.")
    location: Location
    appliances: List[Appliance] = Field(..., min_length=1, description="A list of appliances to be powered.")
    autonomous_days: Optional[int] = Field(2, gt=0, description="Number of days the system should run without sun.")
