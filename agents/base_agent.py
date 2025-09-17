from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

from pydantic import ValidationError


logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return results"""
        pass
    
    def validate_input(self, input_data: Dict[str, Any], required_fields: list) -> None:
        """Validate required input fields"""
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            raise ValidationError(f"{self.name}: Missing required fields: {missing_fields}")