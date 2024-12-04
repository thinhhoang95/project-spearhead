import numpy as np
from typing import List, Union

class FlightPlan:
    def __init__(
        self,
        waypoints: Union[List[List[float]], np.ndarray],
        altitudes: Union[List[int], np.ndarray],
        speeds: Union[List[float], np.ndarray],
        aircraft_category: str,
        delay_allowance: float = 0,
        preference_rank: int = 1
    ):
        """
        Initialize a FlightPlan object.
        
        Args:
            waypoints: n x 2 matrix where each row is [longitude, latitude], in degrees
            altitudes: List of flight levels for each waypoint
            speeds: List of speeds in knots for each waypoint
            aircraft_category: Aircraft category string
            delay_allowance: Maximum allowed delay in seconds
            preference_rank: Rank of preference (lower is more preferred)
        """
        self._waypoints = np.array(waypoints)
        self._validate_waypoints()
        
        self._altitudes = np.array(altitudes)
        self._speeds = np.array(speeds)
        self._validate_dimensions()
        
        self._aircraft_category = aircraft_category
        self._delay_allowance = max(0, delay_allowance)  # Cannot be negative
        self._preference_rank = max(1, int(preference_rank))  # Minimum rank is 1

        
    
    def _validate_waypoints(self):
        """Validate waypoints format and values."""
        if self._waypoints.shape[1] != 2:
            raise ValueError("Waypoints must be a n x 2 matrix")
        
        # Check longitude bounds (-180 to 180)
        if not np.all((-180 <= self._waypoints[:, 0]) & (self._waypoints[:, 0] <= 180)):
            raise ValueError("Longitude must be between -180 and 180 degrees")
        
        # Check latitude bounds (-90 to 90)
        if not np.all((-90 <= self._waypoints[:, 1]) & (self._waypoints[:, 1] <= 90)):
            raise ValueError("Latitude must be between -90 and 90 degrees")
    
    def _validate_dimensions(self):
        """Validate that altitudes and speeds match waypoints length."""
        n_points = len(self._waypoints)
        if len(self._altitudes) != n_points:
            raise ValueError("Number of altitudes must match number of waypoints")
        if len(self._speeds) != n_points:
            raise ValueError("Number of speeds must match number of waypoints")
    
    @property
    def waypoints(self) -> np.ndarray:
        """Get the waypoints array."""
        return self._waypoints.copy()
    
    @property
    def altitudes(self) -> np.ndarray:
        """Get the flight levels array."""
        return self._altitudes.copy()
    
    @property
    def speeds(self) -> np.ndarray:
        """Get the speeds array in knots."""
        return self._speeds.copy()
    
    @property
    def aircraft_category(self) -> str:
        """Get the aircraft category."""
        return self._aircraft_category
    
    @property
    def delay_allowance(self) -> float:
        """Get the delay allowance in seconds."""
        return self._delay_allowance
    
    @property
    def preference_rank(self) -> int:
        """Get the preference rank."""
        return self._preference_rank
    
    def __len__(self) -> int:
        """Return the number of waypoints in the flight plan."""
        return len(self._waypoints)
    
    def __str__(self) -> str:
        """Return a string representation of the flight plan."""
        return (f"FlightPlan with {len(self)} waypoints\n"
                f"Aircraft Category: {self._aircraft_category}\n"
                f"Delay Allowance: {self._delay_allowance} seconds\n"
                f"Preference Rank: {self._preference_rank}")


# Example usage
# waypoints = [[0, 0], [10, 20], [30, 40]]  # longitude, latitude pairs
# altitudes = [300, 350, 370]  # flight levels
# speeds = [450, 460, 440]  # knots
# flight_plan = FlightPlan(
#     waypoints=waypoints,
#     altitudes=altitudes,
#     speeds=speeds,
#     aircraft_category="Heavy",
#     delay_allowance=300,  # 5 minutes
#     preference_rank=2
# )