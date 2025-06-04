"""
Histogram data processor for complex analysis.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict


class HistogramProcessor:
    """
    Specialized processor for histogram complex data.
    
    Handles complex size calculations, time series processing,
    and statistical analysis of complex distributions.
    """
    
    def __init__(self):
        self._cache = {}
    
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

    def calculate_time_series_statistics(self, 
                                       histogram_data: Dict[str, Any], 
                                       legends: List[List[str]],
                                       legend_names: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Calculate time series statistics (mean, std, median) for different legends.
        
        This method processes histogram data across multiple simulations and time points
        to generate statistical measures for each legend over time.
        
        Parameters:
            histogram_data (Dict[str, Any]): Processed histogram data from get_histogram_data()
            legends (List[List[str]]): List of legend definitions, where each legend is a list of species.
                Example: [["A"], ["B"], ["A", "B"]] for separate A, B, and combined A+B analysis
            legend_names (Optional[List[str]]): Custom names for each legend. If None, auto-generated.
                Example: ["Species_A", "Species_B", "Combined_AB"]
        
        Returns:
            pd.DataFrame: DataFrame with columns:
                - Time (s): Time points
                - For each legend: {legend_name}_Mean, {legend_name}_Std, {legend_name}_Median
                
        Example:
            # Get time series statistics for individual and combined species
            legends = [["A"], ["B"], ["A", "B"]]
            legend_names = ["Species_A", "Species_B", "Combined_AB"]
            stats_df = processor.calculate_time_series_statistics(data, legends, legend_names)
            
            # Results in DataFrame with columns:
            # Time (s), Species_A_Mean, Species_A_Std, Species_A_Median, 
            # Species_B_Mean, Species_B_Std, Species_B_Median,
            # Combined_AB_Mean, Combined_AB_Std, Combined_AB_Median
        """
        cache_key = f"time_series_stats_{hash(tuple(tuple(leg) for leg in legends))}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        raw_data = histogram_data['raw_data']
        if not raw_data:
            return pd.DataFrame()
        
        # Generate legend names if not provided
        if legend_names is None:
            legend_names = []
            for i, legend in enumerate(legends):
                if len(legend) == 1:
                    legend_names.append(f"Species_{legend[0]}")
                else:
                    legend_names.append(f"Combined_{'_'.join(legend)}")
        
        if len(legend_names) != len(legends):
            raise ValueError("Number of legend_names must match number of legends")
        
        # Find common time points across all simulations
        time_series_list = [data['time_series'] for data in raw_data if data['time_series']]
        if not time_series_list:
            return pd.DataFrame()
        
        # Use the shortest time series to ensure alignment
        min_length = min(len(ts) for ts in time_series_list)
        common_time_points = time_series_list[0][:min_length]
        
        # Initialize result dictionary
        result_data = {'Time (s)': common_time_points}
        
        # Process each legend
        for legend_idx, (legend, legend_name) in enumerate(zip(legends, legend_names)):
            # Calculate complex sizes for each simulation at each time point
            sim_time_series = []
            
            for data in raw_data:
                if not data['time_series'] or len(data['time_series']) < min_length:
                    continue
                    
                time_series = []
                for time_idx in range(min_length):
                    complexes = data['complexes'][time_idx]
                    
                    # Calculate sizes for all complexes at this time point
                    sizes_at_time = []
                    for count, species_dict in complexes:
                        size = sum(species_dict.get(s, 0) for s in legend if s in species_dict)
                        if size > 0:  # Only include non-zero sizes
                            sizes_at_time.extend([size] * count)
                    
                    time_series.append(sizes_at_time)
                
                sim_time_series.append(time_series)
            
            if not sim_time_series:
                # No valid data for this legend
                result_data[f"{legend_name}_Mean"] = [0.0] * len(common_time_points)
                result_data[f"{legend_name}_Std"] = [0.0] * len(common_time_points)
                result_data[f"{legend_name}_Median"] = [0.0] * len(common_time_points)
                continue
            
            # Calculate statistics across simulations for each time point
            mean_series = []
            std_series = []
            median_series = []
            
            for time_idx in range(min_length):
                # Collect all sizes from all simulations at this time point
                all_sizes_at_time = []
                
                for sim_series in sim_time_series:
                    if time_idx < len(sim_series):
                        all_sizes_at_time.extend(sim_series[time_idx])
                
                if all_sizes_at_time:
                    sizes_array = np.array(all_sizes_at_time)
                    mean_series.append(float(np.mean(sizes_array)))
                    std_series.append(float(np.std(sizes_array)))
                    median_series.append(float(np.median(sizes_array)))
                else:
                    mean_series.append(0.0)
                    std_series.append(0.0)
                    median_series.append(0.0)
            
            # Add to result data
            result_data[f"{legend_name}_Mean"] = mean_series
            result_data[f"{legend_name}_Std"] = std_series
            result_data[f"{legend_name}_Median"] = median_series
        
        # Create DataFrame
        stats_df = pd.DataFrame(result_data)
        
        # Cache the result
        self._cache[cache_key] = stats_df
        
        return stats_df
    
    def calculate_aggregated_statistics(self, 
                                      histogram_data: Dict[str, Any], 
                                      legends: List[List[str]],
                                      legend_names: Optional[List[str]] = None,
                                      time_frame: Optional[Tuple[float, float]] = None) -> pd.DataFrame:
        """
        Calculate aggregated statistics for legends over a specified time frame.
        
        Parameters:
            histogram_data (Dict[str, Any]): Processed histogram data
            legends (List[List[str]]): List of legend definitions
            legend_names (Optional[List[str]]): Custom names for legends
            time_frame (Optional[Tuple[float, float]]): Time range to aggregate over (start, end)
        
        Returns:
            pd.DataFrame: DataFrame with aggregated statistics for each legend
        """
        time_series_df = self.calculate_time_series_statistics(histogram_data, legends, legend_names)
        
        if time_series_df.empty:
            return pd.DataFrame()
        
        # Filter by time frame if specified
        if time_frame is not None:
            start_time, end_time = time_frame
            mask = (time_series_df['Time (s)'] >= start_time) & (time_series_df['Time (s)'] <= end_time)
            filtered_df = time_series_df[mask]
        else:
            filtered_df = time_series_df
        
        if filtered_df.empty:
            return pd.DataFrame()
        
        # Generate legend names if not provided
        if legend_names is None:
            legend_names = []
            for legend in legends:
                if len(legend) == 1:
                    legend_names.append(f"Species_{legend[0]}")
                else:
                    legend_names.append(f"Combined_{'_'.join(legend)}")
        
        # Calculate aggregated statistics
        agg_stats = []
        for legend_name in legend_names:
            mean_col = f"{legend_name}_Mean"
            std_col = f"{legend_name}_Std"
            median_col = f"{legend_name}_Median"
            
            if mean_col in filtered_df.columns:
                stats = {
                    'Legend': legend_name,
                    'Overall_Mean': filtered_df[mean_col].mean(),
                    'Overall_Std': filtered_df[std_col].mean(),
                    'Overall_Median': filtered_df[median_col].mean(),
                    'Time_Avg_Mean': filtered_df[mean_col].mean(),
                    'Time_Avg_Std': filtered_df[mean_col].std(),
                    'Max_Mean': filtered_df[mean_col].max(),
                    'Min_Mean': filtered_df[mean_col].min(),
                    'Final_Mean': filtered_df[mean_col].iloc[-1] if len(filtered_df) > 0 else 0,
                    'Initial_Mean': filtered_df[mean_col].iloc[0] if len(filtered_df) > 0 else 0,
                    'Data_Points': len(filtered_df)
                }
                agg_stats.append(stats)
        
        return pd.DataFrame(agg_stats)
    
    def export_time_series_statistics(self, 
                                    histogram_data: Dict[str, Any], 
                                    legends: List[List[str]],
                                    output_path: str,
                                    legend_names: Optional[List[str]] = None) -> str:
        """
        Export time series statistics to CSV file.
        
        Parameters:
            histogram_data (Dict[str, Any]): Processed histogram data
            legends (List[List[str]]): List of legend definitions
            output_path (str): Path for output CSV file
            legend_names (Optional[List[str]]): Custom names for legends
        
        Returns:
            str: Path to the saved CSV file
        """
        stats_df = self.calculate_time_series_statistics(histogram_data, legends, legend_names)
        
        if stats_df.empty:
            raise ValueError("No data available to export")
        
        # Ensure output directory exists
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to CSV
        stats_df.to_csv(output_path, index=False)
        
        return output_path
    
    def get_legend_comparison_stats(self, 
                                  histogram_data: Dict[str, Any], 
                                  legends: List[List[str]],
                                  legend_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Compare statistics between different legends.
        
        Parameters:
            histogram_data (Dict[str, Any]): Processed histogram data
            legends (List[List[str]]): List of legend definitions to compare
            legend_names (Optional[List[str]]): Custom names for legends
        
        Returns:
            Dict[str, Any]: Comparison statistics between legends
        """
        time_series_df = self.calculate_time_series_statistics(histogram_data, legends, legend_names)
        
        if time_series_df.empty:
            return {}
        
        # Generate legend names if not provided
        if legend_names is None:
            legend_names = []
            for legend in legends:
                if len(legend) == 1:
                    legend_names.append(f"Species_{legend[0]}")
                else:
                    legend_names.append(f"Combined_{'_'.join(legend)}")
        
        comparison_stats = {
            'correlations': {},
            'relative_ratios': {},
            'dominance_analysis': {}
        }
        
        # Calculate correlations between legend means
        mean_columns = [f"{name}_Mean" for name in legend_names]
        available_means = [col for col in mean_columns if col in time_series_df.columns]
        
        if len(available_means) > 1:
            corr_matrix = time_series_df[available_means].corr()
            comparison_stats['correlations'] = corr_matrix.to_dict()
        
        # Calculate relative ratios (if applicable)
        if len(available_means) == 2:
            col1, col2 = available_means
            ratio_series = time_series_df[col1] / (time_series_df[col2] + 1e-10)  # Add small value to avoid division by zero
            comparison_stats['relative_ratios'] = {
                f'{col1}_to_{col2}_ratio': {
                    'mean': float(ratio_series.mean()),
                    'std': float(ratio_series.std()),
                    'median': float(ratio_series.median())
                }
            }
        
        # Dominance analysis (which legend has higher values most of the time)
        if len(available_means) > 1:
            dominance = {}
            for i, col1 in enumerate(available_means):
                for j, col2 in enumerate(available_means):
                    if i < j:  # Avoid duplicate comparisons
                        dominance_count = (time_series_df[col1] > time_series_df[col2]).sum()
                        total_points = len(time_series_df)
                        dominance[f'{col1}_dominates_{col2}'] = dominance_count / total_points
            
            comparison_stats['dominance_analysis'] = dominance
        
        return comparison_stats

    def clear_cache(self):
        """Clear processor cache."""
        self._cache.clear()