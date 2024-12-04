from typing import List, Optional
from .FlightPlan import FlightPlan

class Flight:
    def __init__(
        self,
        callsign: str,
        airline: str,
        aircraft: str,
        wake_turbulence_cat: str,
        cost_index: float,
        filed_plans: Optional[List[FlightPlan]] = None
    ):
        """
        Initialize a Flight object.
        
        Args:
            callsign: Flight callsign (e.g., 'UAL123')
            airline: Operating airline (e.g., 'United Airlines')
            aircraft: Aircraft type (e.g., 'B738')
            wake_turbulence_cat: Wake turbulence category ('Light', 'Medium', 'Heavy', 'Super')
            cost_index: Cost index value for flight optimization
            filed_plans: List of potential FlightPlan objects, ordered by preference
        """
        self._callsign = callsign
        self._airline = airline
        self._aircraft = aircraft
        self._validate_wake_category(wake_turbulence_cat)
        self._wake_turbulence_cat = wake_turbulence_cat
        self._cost_index = float(cost_index)
        self._filed_plans = filed_plans if filed_plans is not None else []

    def _validate_wake_category(self, category: str):
        """Validate the wake turbulence category."""
        valid_categories = {'Light', 'Medium', 'Heavy', 'Super'}
        if category not in valid_categories:
            raise ValueError(f"Wake turbulence category must be one of {valid_categories}")

    @property
    def callsign(self) -> str:
        """Get the flight callsign."""
        return self._callsign

    @property
    def airline(self) -> str:
        """Get the operating airline."""
        return self._airline

    @property
    def aircraft(self) -> str:
        """Get the aircraft type."""
        return self._aircraft

    @property
    def wake_turbulence_cat(self) -> str:
        """Get the wake turbulence category."""
        return self._wake_turbulence_cat

    @property
    def cost_index(self) -> float:
        """Get the cost index."""
        return self._cost_index

    @property
    def filed_plans(self) -> List[FlightPlan]:
        """Get the list of filed flight plans."""
        return self._filed_plans.copy()

    def add_flight_plan(self, flight_plan: FlightPlan):
        """
        Add a flight plan to the list of filed plans.
        
        Args:
            flight_plan: FlightPlan object to add
        """
        self._filed_plans.append(flight_plan)

    def __str__(self) -> str:
        """Return a string representation of the flight."""
        return (f"Flight {self._callsign}\n"
                f"Airline: {self._airline}\n"
                f"Aircraft: {self._aircraft}\n"
                f"Wake Category: {self._wake_turbulence_cat}\n"
                f"Cost Index: {self._cost_index}\n"
                f"Number of Filed Plans: {len(self._filed_plans)}")

# Example usage:
# flight = Flight(
#     callsign="UAL123",
#     airline="United Airlines",
#     aircraft="B738",
#     wake_turbulence_cat="Medium",
#     cost_index=25
# )
# flight.add_flight_plan(flight_plan)
