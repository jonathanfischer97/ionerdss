"""
Histogram data processor for complex analysis.
"""

import numpy as np
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
    
    def calculate_monomer_counts(self, 
                               histogram_data: Dict[str, Any], 
                               legend: List[str]) -> List[List[Tuple[int, int]]]:
        """Calculate (size, monomer_count) pairs for specified species."""
        all_data = []
        for data in histogram_data['raw_data']:
            sim_data = []
            for complexes in data['complexes']:
                for count, species_dict in complexes:
                    size = sum(species_dict.get(s, 0) for s in legend if s in species_dict)
                    sim_data.append((size, count * size))
            all_data.append(sim_data)
        return all_data
    
    def get_time_binned_data(self, 
                           histogram_data: Dict[str, Any], 
                           legend: List[str],
                           time_bins: int = 10) -> Dict[str, np.ndarray]:
        """Bin histogram data by time intervals."""
        all_time_size_pairs = []
        
        for data in histogram_data['raw_data']:
            for i, time in enumerate(data['time_series']):
                for count, species_dict in data['complexes'][i]:
                    size = sum(species_dict.get(s, 0) for s in legend if s in species_dict)
                    all_time_size_pairs.extend([(time, size)] * count)
        
        if not all_time_size_pairs:
            return {'times': np.array([]), 'sizes': np.array([]), 'counts': np.array([])}
        
        times, sizes = zip(*all_time_size_pairs)
        time_min, time_max = min(times), max(times)
        size_min, size_max = min(sizes), max(sizes)
        
        time_edges = np.linspace(time_min, time_max, time_bins + 1)
        size_edges = np.arange(size_min, size_max + 2)
        
        hist2d, _, _ = np.histogram2d(times, sizes, bins=[time_edges, size_edges])
        
        return {
            'hist2d': hist2d,
            'time_edges': time_edges,
            'size_edges': size_edges,
            'time_centers': (time_edges[:-1] + time_edges[1:]) / 2,
            'size_centers': (size_edges[:-1] + size_edges[1:]) / 2
        }
    
    def calculate_species_composition(self, 
                                    histogram_data: Dict[str, Any]) -> Dict[str, List[Dict[str, int]]]:
        """Calculate species composition for each complex type."""
        compositions = defaultdict(list)
        
        for data in histogram_data['raw_data']:
            sim_compositions = []
            for complexes in data['complexes']:
                for count, species_dict in complexes:
                    sim_compositions.extend([species_dict] * count)
            compositions[f"sim_{len(compositions)}"] = sim_compositions
        
        return dict(compositions)
    
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
    
    def filter_by_species_condition(self, 
                                   histogram_data: Dict[str, Any], 
                                   condition: str) -> Dict[str, Any]:
        """Filter complexes by species condition (e.g., 'A>=2', 'B==1')."""
        import re
        
        # Parse condition
        match = re.match(r'(\w+)([><=!]+)(\d+)', condition)
        if not match:
            raise ValueError(f"Invalid condition format: {condition}")
        
        species, operator, threshold = match.groups()
        threshold = int(threshold)
        
        filtered_data = []
        for data in histogram_data['raw_data']:
            filtered_complexes = []
            for complexes in data['complexes']:
                filtered_time_complexes = []
                for count, species_dict in complexes:
                    species_count = species_dict.get(species, 0)
                    
                    if self._evaluate_condition(species_count, operator, threshold):
                        filtered_time_complexes.append((count, species_dict))
                
                filtered_complexes.append(filtered_time_complexes)
            
            filtered_data.append({
                'time_series': data['time_series'],
                'complexes': filtered_complexes
            })
        
        return {
            'raw_data': filtered_data,
            'condition': condition,
            'metadata': histogram_data['metadata']
        }
    
    def _evaluate_condition(self, value: int, operator: str, threshold: int) -> bool:
        """Evaluate condition based on operator."""
        if operator == '>=':
            return value >= threshold
        elif operator == '>':
            return value > threshold
        elif operator == '<=':
            return value <= threshold
        elif operator == '<':
            return value < threshold
        elif operator == '==' or operator == '=':
            return value == threshold
        elif operator == '!=':
            return value != threshold
        else:
            raise ValueError(f"Unknown operator: {operator}")
    
    def clear_cache(self):
        """Clear processor cache."""
        self._cache.clear()