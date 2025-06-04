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

    def clear_cache(self):
        """Clear processor cache."""
        self._cache.clear()