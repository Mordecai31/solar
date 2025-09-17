import pytest
import json
from pydantic import ValidationError
from solar_project.agents.input_validation_agent import InputValidationAgent
from solar_project.data.schemas.user_input_schemas import UserInput

# It's good practice to have a fixtures file, but for now, we can define it here.
# A better approach would be to move this to tests/conftest.py
@pytest.fixture
def valid_user_input_data():
    """Provides a valid user input dictionary for testing."""
    # Using the sample file we created
    with open("solar_project/data/sample/sample_user_inputs.json", "r") as f:
        return json.load(f)

@pytest.fixture
def validation_agent():
    """Provides an instance of the InputValidationAgent."""
    return InputValidationAgent()

def test_validate_valid_input(validation_agent, valid_user_input_data):
    """
    Tests that the InputValidationAgent correctly validates a valid input dictionary.
    """
    # Act
    validated_data = validation_agent.validate(valid_user_input_data)

    # Assert
    assert isinstance(validated_data, UserInput)
    assert validated_data.budget == 5000000.0
    assert validated_data.location.state == "Lagos"
    assert len(validated_data.appliances) == 4

@pytest.mark.parametrize("invalid_data_update, field_to_del", [
    ({"budget": -100}, None),
    ({"appliances": []}, None),
    ({"appliances": [{"name": "Fridge", "wattage": -50, "hours_per_day": 12, "quantity": 1}]}, None),
    (None, "location"),
    ({"location": {"state": ""}}, None), # Empty state
    ({"appliances": [{"name": "TV", "wattage": 100, "hours_per_day": 25, "quantity": 1}]}, None), # Invalid hours
])
def test_validate_invalid_input(validation_agent, valid_user_input_data, invalid_data_update, field_to_del):
    """
    Tests that the InputValidationAgent raises a ValidationError for various invalid inputs.
    """
    # Arrange
    invalid_data = valid_user_input_data.copy()
    if invalid_data_update:
        invalid_data.update(invalid_data_update)
    if field_to_del:
        del invalid_data[field_to_del]

    # Act & Assert
    with pytest.raises(ValidationError):
        validation_agent.validate(invalid_data)

def test_missing_required_field(validation_agent, valid_user_input_data):
    """
    Tests that a missing required field raises a ValidationError.
    """
    # Arrange
    invalid_data = valid_user_input_data.copy()
    del invalid_data["budget"] # budget is a required field

    # Act & Assert
    with pytest.raises(ValidationError):
        validation_agent.validate(invalid_data)
