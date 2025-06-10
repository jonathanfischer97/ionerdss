"""
Histogram data processor for complex analysis.
"""
import os
import numpy as np
import re
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional

# Helper functions
from utils import parse_histogram_complex, parse_histogram_line, filter_by_time_frame, align_time_series


# Configure logging, 
import logging
# inherit from the global level (should be setup in main)
logger = logging.getLogger(__name__)



class HistogramProcessor:
    """
    Specialized processor for histogram complex data.
    
    Handles complex size calculations, time series processing,
    and statistical analysis of complex distributions.
    """
    
    def __init__(self):
        self._cache = {}
        self._selected_dirs = []

    def configure(self, selected_dirs: List[str]):
        self._selected_dirs = selected_dirs

    def read(self, selected_dirs: List[str]) -> List[Dict[str, Any]]:
        """Nick name for read_multiple"""
        return self.read_multiple(self, selected_dirs)
    
    def read_single(sim_dir: str) -> Dict[str, Any]:
        """
        Read histogram complex data from a simulation directory.
        
        Parameters:
            sim_dir (str): Path to the simulation directory
            
        Returns:
            Dict[str, Any]: Dictionary containing time series and complex data
        """
        data_file = os.path.join(sim_dir, "DATA", "histogram_complexes_time.dat")
        
        if not os.path.exists(data_file):
            logger.warning(f"Histogram complexes file not found: {data_file}")
            return {"time_series": [], "complexes": []}
        
        time_series = []
        all_complexes = []
        
        try:
            with open(data_file, "r") as f:
                lines = f.readlines()
            
            current_time = None
            current_complexes = []
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                    
                time_match = re.match(r"Time \(s\): (\d*\.?\d+)", line)
                if time_match:
                    if current_time is not None:
                        time_series.append(current_time)
                        all_complexes.append(current_complexes)
                        current_complexes = []
                    
                    current_time = float(time_match.group(1))
                else:
                    count, species_dict = parse_histogram_line(line)
                    if species_dict:
                        current_complexes.append((count, species_dict))
                    elif line.strip() and not line.startswith('#'):
                        logger.debug(f"Could not parse line {line_num}: {line}")
            
            # Add the last time point
            if current_time is not None and current_complexes:
                time_series.append(current_time)
                all_complexes.append(current_complexes)
            
            logger.debug(f"Successfully read histogram complexes from {data_file}")
            
        except Exception as e:
            logger.error(f"Error reading histogram complexes from {data_file}: {e}")
            return {"time_series": [], "complexes": []}
        
        return {
            "time_series": time_series,
            "complexes": all_complexes
        }

    def read_multiple(self, selected_dirs: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """read multiple files"""

        # check cache
        cache_key = "raw_data"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        if not selected_dirs:
            if not self._selected_dirs:
                raise FileNotFoundError("No directory selected for reading.")
            selected_dirs = self._selected_dirs

        # Load raw data
        all_data = []
        for sim_dir in selected_dirs:
            data = self.read(sim_dir)
            if data["time_series"]:
                if self._config['time_frame']:
                    data = filter_by_time_frame(data, self._config['time_frame'])
                all_data.append(data)

        self._cache[cache_key] = all_data

        return all_data

    def calculate_complex_sizes(self, 
                              histogram_data: Dict[str, Any], 
                              legend: List[str]) -> List[List[int]]:
        """Calculate complex sizes for specified species across all simulations."""
        cache_key = f"sizes_{hash(tuple(legend))}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        all_sizes = []
        for data in histogram_data['raw_data']:
            sim_sizes = []
            for complexes in data['complexes']:
                for count, species_dict in complexes:
                    size = sum(species_dict.get(s, 0) for s in legend if s in species_dict)
                    sim_sizes.extend([size] * count)
            all_sizes.append(sim_sizes)
        
        self._cache[cache_key] = all_sizes
        return all_sizes
    
    
    def get_size_distribution_stats(self, 
                                  histogram_data: Dict[str, Any], 
                                  legend: List[str]) -> Dict[str, float]:
        """Calculate statistical measures of size distribution."""
        all_sizes = self.calculate_complex_sizes(histogram_data, legend)
        combined_sizes = [size for sim_sizes in all_sizes for size in sim_sizes]
        
        if not combined_sizes:
            return {'mean': 0, 'std': 0, 'median': 0, 'max': 0, 'min': 0}
        
        sizes_array = np.array(combined_sizes)
        return {
            'mean': float(np.mean(sizes_array)),
            'std': float(np.std(sizes_array)),
            'median': float(np.median(sizes_array)),
            'max': int(np.max(sizes_array)),
            'min': int(np.min(sizes_array)),
            'total_complexes': len(combined_sizes)
        }
    
    def get_time_series(self, 
                        legends: List[List[str]],
                        legend_names: Optional[List[str]] = None
        ) -> pd.DataFrame:

        """
        Calculate time series statistics (mean, std, median) for different legends.
        
        This method processes histogram data across multiple simulations and time points
        to generate statistical measures for each legend over time.
        
        Parameters:
            histogram_data (Dict[str, Any]): Processed histogram data from get_histogram_data()
            legends (List[List[str]]): List of legend definitions, where each legend is a list of species.
                Example: ["A: 1.", "B: 2.", "A: 3. B: 4."] for separate A, B, and combined A+B analysis
            legend_names (Optional[List[str]]): Custom names for each legend. If None, use legends.
                Example: ["A1", "B2", "A3B4"]
        
        Returns:
            pd.DataFrame: DataFrame with columns:
                - Time (s): Time points
                - For each legend: Each trajectory's data for aligned time points
                
        Example:
            # Get time series statistics for individual and combined species
            legends = ["A: 1.", "B: 2.", "A: 3. B: 4."]
            legend_names = ["A1", "B2", "A3B4"]
            stats_df = processor.get_time_series(data, legends, legend_names)
        """
        cache_key = f"time_series_{hash(tuple(tuple(leg) for leg in legends))}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        cache_key = f"raw_data"
        if cache_key in self._cache:
            raw_data = self._cache[cache_key]
        else:
            logger.warning("No data read. Start reading...")
            try:
                raw_data = self.read_multiple()
            except Exception as e:
                logger.error(f"No data provided: {e}")
        
        # Generate legend names if not provided
        if legend_names is None:
            legend_names = legends
        
        if len(legend_names) != len(legends):
            raise ValueError("Number of legend_names must match number of legends")
        
        legend_dicts = [parse_histogram_complex(l) for l in legends]
        
        common_time_points = align_time_series(raw_data)
        min_length = len(common_time_points)
        
        # Initialize result dictionary
        result_data = {'Time (s)': common_time_points}
        for ldict in legend_dicts:
            result_data[ldict] = [] # all data points
        
        # Process over all data
            
        for data in raw_data:
            if not data['time_series'] or len(data['time_series']) < min_length:
                logger.critical(f"Illegal time_series. This should not happen. Min length calculated is {min_length}. \n" +
                                f"This time series has length {len(data['time_series'])}")
                continue
                
            time_series = {}
            for ldict in legend_dicts:
                time_series[ldict] = []

            for time_idx in range(min_length):
                complexes = data['complexes'][time_idx]
                
                # Calculate sizes for all complexes at this time point
                sizes_at_time = []
                for count, species_dict in complexes:
                    if species_dict in legend_dicts:
                        time_series[ldict].append(count)
            
            result_data[ldict].append(time_series[ldict])

        self._cache[cache_key] = result_data

        return result_data
        

    def calculate_time_series_statistics(self, 
                                       legends: List[List[str]],
                                       legend_names: Optional[List[str]] = None) -> Dict[Dict,Any]:
        """
        Calculate time series statistics (mean, std, median) for different legends.
        
        This method processes histogram data across multiple simulations and time points
        to generate statistical measures for each legend over time.
        
        Parameters:
            histogram_data (Dict[str, Any]): Processed histogram data from get_histogram_data()
            legends (List[List[str]]): List of legend definitions, where each legend is a list of species.
                Example: ["A: 1.", "B: 2.", "A: 3. B: 4."] for separate A, B, and combined A+B analysis
            legend_names (Optional[List[str]]): Custom names for each legend. If None, use legends.
                Example: ["A1", "B2", "A3B4"]
        
        Returns:
            pd.DataFrame: DataFrame with columns:
                - Time (s): Time points
                - For each legend: {legend_name}_Mean, {legend_name}_Std, {legend_name}_Median
                
        Example:
            # Get time series statistics for individual and combined species
            legends = ["A: 1.", "B: 2.", "A: 3. B: 4."]
            legend_names = ["A1", "B2", "A3B4"]
            stats_df = processor.calculate_time_series_statistics(data, legends, legend_names)
            
            # Results in DataFrame with columns:
            # Time (s), Species_A_Mean, Species_A_Std, Species_A_Median, 
            # Species_B_Mean, Species_B_Std, Species_B_Median,
            # Combined_AB_Mean, Combined_AB_Std, Combined_AB_Median
        """
        cache_key = f"time_series_stats_{hash(tuple(tuple(leg) for leg in legends))}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try: # to get the time series
            result_data = self.get_time_series(legends, legend_names)
        except Exception as e:
            logger.error("Error getting time series: {e}")
            
        
        # Calculate statistics across simulations for each time point
        result_stat = {'Time (s)': result_data['Time (s)']}
        legend_names = [key for key in result_stat if key != 'Time (s)']
        try:
            for species in legend_names:
                result_stat[species] = {
                    'mean':np.mean(result_data[species], axis=0), 
                    'std':np.std(result_data[species], axis=0), 
                    'median':np.median(result_data[species], axis=0),
                }
        except Exception as e:
            logger.error("Failed calculating stats: {e}")
        
        # Cache the result
        self._cache[cache_key] = result_stat
        
        return result_stat

    def clear_cache(self):
        """Clear processor cache."""
        self._cache.clear()

