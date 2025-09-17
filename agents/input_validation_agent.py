from .base_agent import BaseAgent
from core.validators import validate_user_input
from core.exceptions import ValidationError
from typing import Any, Dict

class InputValidationAgent(BaseAgent):
    """Validates user input data"""
    
    def __init__(self):
        super().__init__("InputValidator")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user input"""
        try:
            validated_data = validate_user_input(input_data)
            self.logger.info("Input validation successful")
            
            return {
                "status": "success",
                "validated_data": validated_data,
                "message": "Input validation passed"
            }
        
        except ValidationError as e:
            self.logger.error(f"Input validation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "message": "Input validation failed"
            }