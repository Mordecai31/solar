from typing import Dict, Any
from solar_project.data.schemas.user_input_schemas import UserInput
from solar_project.core.calculations import calculate_total_daily_load_wh

class LoadCalculatorAgent:
    """
    An agent responsible for calculating the total energy load based on user input.
    """

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates the total daily load and adds it to the state.

        Args:
            state: A dictionary representing the current state of the workflow.
                   It is expected to contain a 'user_input' key with a
                   validated UserInput object.

        Returns:
            The updated state dictionary with a new 'total_daily_load_wh' key.

        Raises:
            KeyError: If 'user_input' is not found in the state.
        """
        print("--- Running Load Calculator Agent ---")

        user_input: UserInput = state.get("user_input")
        if not user_input:
            raise KeyError("State must contain a 'user_input' key with a validated UserInput object.")

        total_load = calculate_total_daily_load_wh(user_input.appliances)

        print(f"Calculated total daily load: {total_load:.2f} Wh")

        state["total_daily_load_wh"] = total_load

        return state
