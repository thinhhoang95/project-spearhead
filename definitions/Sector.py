import numpy as np
from typing import List, Tuple

from dotenv import load_dotenv
import os

load_dotenv()
DEBUG_LEVEL = int(os.getenv('DEBUG_LEVEL', '0'))


class Sector:
    """
    A class representing an airspace sector with its geographical boundaries and capacity constraints.
    
    Attributes:
        name (str): The name/identifier of the sector
        polygon (List[Tuple[float, float]]): List of (latitude, longitude) coordinates defining the sector boundaries
        capacity (np.ndarray): 96-element array representing 15-minute capacity slots throughout the day
        centroid (Tuple[float, float]): The centroid of the sector
    """
    
    def __init__(self, name: str, polygon: List[Tuple[float, float]], capacity: np.ndarray = None,
                 centroid: Tuple[float, float] = None, lower_altitude: float = None, upper_altitude: float = None):
        """
        Initialize a Sector object.
        
        Args:
            name: The sector's name or identifier
            polygon: List of (latitude, longitude) tuples defining the sector boundaries
            capacity: Optional 96-element numpy array for capacity. If None, defaults to zeros
            centroid: Optional tuple (latitude, longitude) for the sector's centroid
            lower_altitude: Optional lower altitude limit for the sector
            upper_altitude: Optional upper altitude limit for the sector
        """
        self.name = name
        self.polygon = polygon
        self.centroid = centroid
        self.lower_altitude = lower_altitude
        self.upper_altitude = upper_altitude
        
        # Initialize capacity as zeros if not provided
        if capacity is None:
            self.capacity = np.zeros(96, dtype=int)
        else:
            if len(capacity) != 96:
                raise ValueError("Capacity must be a 96-element array (15-minute intervals for 24 hours)")
            self.capacity = capacity

    def set_capacity(self, time_index: int, value: int) -> None:
        """
        Set the capacity for a specific time slot.
        
        Args:
            time_index: Index (0-95) representing the 15-minute time slot
            value: The capacity value to set
        """
        if not 0 <= time_index < 96:
            raise ValueError("Time index must be between 0 and 95")
        self.capacity[time_index] = value

    def get_capacity(self, time_index: int) -> int:
        """
        Get the capacity for a specific time slot.
        
        Args:
            time_index: Index (0-95) representing the 15-minute time slot
            
        Returns:
            The capacity value for the specified time slot
        """
        if not 0 <= time_index < 96:
            raise ValueError("Time index must be between 0 and 95")
        return self.capacity[time_index]
    
    def get_centroid(self) -> Tuple[float, float]:
        """
        Get the centroid of the sector (latitude, longitude)
        """
        return self.centroid
    
    def get_lower_altitude(self) -> float:
        """
        Get the lower altitude limit of the sector
        """
        return self.lower_altitude
    
    def get_upper_altitude(self) -> float:
        """
        Get the upper altitude limit of the sector
        """
        return self.upper_altitude

    def __str__(self) -> str:
        """String representation of the Sector."""
        return f"Sector {self.name} with {len(self.polygon)} boundary points"

    def __repr__(self) -> str:
        """Detailed string representation of the Sector."""
        return f"Sector(name='{self.name}', polygon={self.polygon}, capacity=array[...])"

def load_sectors_from_traffic() -> List[Sector]:
    """
    Load sectors from EURO FIRs using the traffic library.
    
    Returns:
        List[Sector]: List of Sector objects representing European FIRs
    """
    # Import eurofirs from traffic.data
    from traffic.data import eurofirs
    
    sectors = []

    eurofirs_df = eurofirs.data
    
    # Iterate through each row in the eurofirs dataframe
    for index, row in eurofirs_df.iterrows():
        # Extract the polygon coordinates
        # The geometry is typically in (longitude, latitude) format
        # but we need (latitude, longitude) for our Sector class
        polygon = row['geometry'] # shapely polygon
        # Extract the coordinates
        polygon_coords = [(lat, lon) for lon, lat in polygon.exterior.coords]
        
        # Create capacity array (default to zeros)
        capacity = np.zeros(96, dtype=int)
        
        # Create a new Sector object
        sector = Sector(
            name=row['designator'],  # Use the FIR designator as the name
            polygon=polygon_coords,
            capacity=capacity,
            centroid=(row['latitude'], row['longitude']),
            lower_altitude=row['lower'],
            upper_altitude=row['upper']
        )
        
        sectors.append(sector)

    if DEBUG_LEVEL >= 2:
        print(f'Loaded {len(sectors)} sectors')

    return sectors

# # Example usage
# import numpy as np

# # Create a sector with some example data
# polygon = [(40.0, -74.0), (41.0, -74.0), (41.0, -73.0), (40.0, -73.0)]
# capacity = np.ones(96) * 10  # Capacity of 10 flights for each 15-minute slot
# sector = Sector("NYC01", polygon, capacity)

# # Get capacity for a specific time slot (e.g., 1:00 AM = index 4)
# capacity_at_1am = sector.get_capacity(4)

# # Set capacity for a specific time slot
# sector.set_capacity(8, 15)  # Set capacity to 15 flights at 2:00 AM