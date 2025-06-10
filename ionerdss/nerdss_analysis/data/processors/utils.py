from typing import List, Dict, Any, Tuple, Optional
import re

# Configure logging, 
import logging
# inherit from the global level (should be setup in main)
logger = logging.getLogger(__name__)

# ========================================================================
# Helper functions
# ========================================================================

def parse_histogram_complex(species_data_str: str) -> Optional[Dict[str, int]]:
    """
    Parse species data string and return a dictionary with species and counts.
    
    Parameters:
        species_data_str (str): Species data like "A: 2. B: 1."
        
    Returns:
        Optional[Dict[str, int]]: Dictionary mapping species to counts, or None if parsing fails
        
    Example:
        >>> parse_histogram_complex("A: 2. B: 1.")
        {'A': 2, 'B': 1}
        
        >>> parse_histogram_complex("A: 3. A: 1.")  # Duplicate species
        {'A': 4}
    """
    species_data = species_data_str.split()
    species_dict = {}

    try:
        for i in range(0, len(species_data), 2):
            species_name = species_data[i].strip(":")
            species_count = int(species_data[i + 1].strip("."))
            species_dict[species_name] = species_dict.get(species_name, 0) + species_count
    except (IndexError, ValueError) as e:
        logger.warning(f"Error parsing species data '{species_data_str}': {e}")
        return None

    return species_dict
     
def parse_histogram_line(line: str) -> Tuple[Optional[int], Optional[Dict[str, int]]]:
    """
    Parse a single complex line and return a dictionary with species and counts.
    
    Parameters:
        line (str): A line of text containing complex data
        
    Returns:
        Tuple[Optional[int], Optional[Dict[str, int]]]: 
            A tuple containing the count of complexes and a dictionary mapping species to counts
            
    Example:
        >>> parse_complex_line("5 A: 2. B: 1.")
        (5, {'A': 2, 'B': 1})
    """
    match = re.match(r"(\d+)\s+([\w\.\s:]+)", line)
    if not match:
        return None, None

    count = int(match.group(1))
    species_data_str = match.group(2)
    
    # Use the new parsing function
    species_dict = parse_histogram_complex(species_data_str)
    
    if species_dict is None:
        logger.warning(f"Error parsing complex line '{line}': failed to parse species data")
        return None, None

    return count, species_dict

def filter_by_time_frame(data: Dict[str, Any], time_frame: Tuple[float, float]) -> Dict[str, Any]:
        """Filter data by time frame."""
        start, end = time_frame
        filtered_indices = [
            i for i, t in enumerate(data["time_series"]) 
            if start <= t <= end
        ]
        
        return {
            "time_series": [data["time_series"][i] for i in filtered_indices],
            "complexes": [data["complexes"][i] for i in filtered_indices]
        }

def align_time_series(all_data: List[Dict[str, Any]]) -> List[float]:
        """
        Find common time points across simulations.
        TODO: Should return the aligned time series and indices for each trajectory.
        """

        time_series_list = [data['time_series'] for data in all_data if data['time_series']]
        if not time_series_list:
            return []
        
        # Use the shortest time series to ensure alignment
        min_length = min(len(ts) for ts in time_series_list)
        common_time_points = time_series_list[0][:min_length]
        
        # Initialize result dictionary
        return common_time_points