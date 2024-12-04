from typing import List, Optional
from datetime import datetime
from .Flight import Flight
from .Sector import Sector

from dotenv import load_dotenv
import os

load_dotenv()

DEBUG_LEVEL = int(os.getenv('DEBUG_LEVEL', '0'))

class Scenario:
    """
    A class representing an air traffic scenario containing flights and sectors.
    
    Attributes:
        name (str): The name/identifier of the scenario
        flights (List[Flight]): List of flights in the scenario
        sectors (List[Sector]): List of sectors in the scenario
        datetime (str): Optional timestamp for the scenario
        author (str): Optional author of the scenario
    """
    
    def __init__(
        self,
        name: str,
        flights: Optional[List[Flight]] = None,
        sectors: Optional[List[Sector]] = None,
        datetime_str: Optional[str] = None,
        author: Optional[str] = None
    ):
        """
        Initialize a Scenario object.
        
        Args:
            name: The scenario's name or identifier
            flights: Optional list of Flight objects
            sectors: Optional list of Sector objects
            datetime_str: Optional datetime string for the scenario
            author: Optional author name
        """
        self.name = name
        self.flights = flights if flights is not None else []
        self.sectors = sectors if sectors is not None else []
        self.datetime = datetime_str
        self.author = author

    def add_flight(self, flight: Flight) -> None:
        """
        Add a flight to the scenario.
        
        Args:
            flight: Flight object to add
        """
        self.flights.append(flight)

    def add_sector(self, sector: Sector) -> None:
        """
        Add a sector to the scenario.
        
        Args:
            sector: Sector object to add
        """
        self.sectors.append(sector)

    def get_flights(self) -> List[Flight]:
        """
        Get all flights in the scenario.
        
        Returns:
            List of Flight objects
        """
        return self.flights.copy()

    def get_sectors(self) -> List[Sector]:
        """
        Get all sectors in the scenario.
        
        Returns:
            List of Sector objects
        """
        return self.sectors.copy()

    def __str__(self) -> str:
        """String representation of the Scenario."""
        return (f"Scenario: {self.name}\n"
                f"Number of flights: {len(self.flights)}\n"
                f"Number of sectors: {len(self.sectors)}\n"
                f"Datetime: {self.datetime or 'Not specified'}\n"
                f"Author: {self.author or 'Not specified'}")

    def __repr__(self) -> str:
        """Detailed string representation of the Scenario."""
        return (f"Scenario(name='{self.name}', "
                f"flights=[{len(self.flights)} flights], "
                f"sectors=[{len(self.sectors)} sectors], "
                f"datetime='{self.datetime}', "
                f"author='{self.author}')")

# Example usage:
# # Create a scenario
# scenario = Scenario(
#     name="Europe_Morning_Rush",
#     datetime_str="2024-03-20 06:00:00",
#     author="John Doe"
# )
# 
# # Add flights and sectors
# scenario.add_flight(flight)
# scenario.add_sector(sector)

import numpy as np
from .FlightPlan import FlightPlan

def load_scenario_from_file(file_name: str) -> Scenario:
    """
    Load a scenario from a YAML file.
    
    Args:
        file_name: Name of the YAML file in the scenarios directory
        
    Returns:
        Scenario object populated with data from the file
    """
    from dotenv import load_dotenv
    import os
    import yaml
    from datetime import datetime

    # Load environment variables
    load_dotenv()
    project_root = os.getenv('PROJECT_ROOT')
    
    # Construct full path to scenario file
    scenario_path = os.path.join(project_root, 'scenarios', file_name)
    
    # Read and parse YAML file
    with open(scenario_path, 'r') as f:
        scenario_data = yaml.safe_load(f)
    
    # Create scenario object with basic info
    scenario = Scenario(
        name=scenario_data.get('name', 'Unnamed Scenario'),
        datetime_str=scenario_data.get('datetime'),
        author=scenario_data.get('author')
    )
    
    # Load flights if present
    if 'flights' in scenario_data:
        for flight_data in scenario_data['flights']:
            flight = Flight(
                callsign=flight_data['callsign'],
                airline=flight_data['airline'],
                aircraft=flight_data['aircraft'],
                wake_turbulence_cat=flight_data['wake_turbulence_cat'],
                cost_index=flight_data['cost_index']
            )
            
            # Add flight plans if present
            if 'filed_plans' in flight_data:
                for plan_data in flight_data['filed_plans']:
                    flight_plan = FlightPlan(
                        waypoints=plan_data['waypoints'],
                        altitudes=plan_data['altitudes'],
                        speeds=plan_data['speeds'],
                        aircraft_category=plan_data['aircraft_category'],
                        delay_allowance=plan_data.get('delay_allowance', 0),
                        preference_rank=plan_data.get('preference_rank', 1)
                    )
                    flight.add_flight_plan(flight_plan)
                    
            scenario.add_flight(flight)
    
    if DEBUG_LEVEL >= 2:
        print(f'Loaded scenario from {file_name}. There were {len(scenario.flights)} flights.')
        
    return scenario