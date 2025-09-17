from pydantic import BaseModel, Field
from typing import List, Optional
from data.schemas.component_schemas import ComponentType


class ComponentRecommendation(BaseModel):
    component_type:ComponentType
    model: str
    specifications: dict
    price: float
    score: float
    reasoning: str

class SystemRecommendation(BaseModel):
    total_cost: float
    daily_energy_need: float
    recommended_components: List[ComponentRecommendation]
    system_performance: dict
    payback_period_years: float
    co2_savings_annually: float