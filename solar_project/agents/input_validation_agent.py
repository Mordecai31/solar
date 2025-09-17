from typing import Dict, Any
from pydantic import ValidationError

# Adjust the import path based on the project structure.
# Assuming the root 'solar_project' is in the Python path.
from solar_project.data.schemas.user_input_schemas import UserInput

class InputValidationAgent:
    """
    An agent responsible for validating the raw user input against the defined Pydantic models.
    """

    def validate(self, user_data: Dict[str, Any]) -> UserInput:
        """
        Validates the user input dictionary.

        Args:
            user_data: A dictionary containing the user's input.

        Returns:
            A validated UserInput object if the data is valid.

        Raises:
            ValidationError: If the user_data does not conform to the UserInput schema.
        """
        try:
            validated_input = UserInput.model_validate(user_data)
            return validated_input
        except ValidationError as e:
            # For now, we'll re-raise the exception.
            # In a real application, we might want to log this or format it
            # for a user-friendly error message.
            print(f"ERROR: Input validation failed: {e}")
            raise

# Example of how this agent might be used:
if __name__ == '__main__':
    sample_valid_data = {
        "budget": 5000000.0,
        "location": {
            "state": "Lagos"
        },
        "appliances": [
            {
                "name": "Refrigerator",
                "wattage": 200,
                "hours_per_day": 24,
                "quantity": 1
            },
            {
                "name": "Air Conditioner",
                "wattage": 1500,
                "hours_per_day": 8,
                "quantity": 2
            }
        ],
        "autonomous_days": 3
    }

    sample_invalid_data = {
        "budget": -100,  # Invalid budget
        "location": {
            "state": "Osun"
        },
        "appliances": []  # Invalid: must have at least one appliance
    }

    validator = InputValidationAgent()

    print("--- Testing with valid data ---")
    try:
        validated_data = validator.validate(sample_valid_data)
        print("Validation successful!")
        print(validated_data)
    except ValidationError as e:
        print(f"Validation failed unexpectedly: {e}")

    print("\n--- Testing with invalid data ---")
    try:
        validator.validate(sample_invalid_data)
    except ValidationError as e:
        print("Validation failed as expected.")
        # print(f"Details: {e}")
