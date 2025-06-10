"""
Core data processing class for ionerdss analysis.
Enhanced with specialized processors for different data types.
"""

import os
import pickle
import hashlib
from typing import List, Optional, Dict, Any, Tuple
from .processors import HistogramProcessor, CopyNumberProcessor, TransitionProcessor

from .processors.utils import align_time_series


class Data:
    """
    Enhanced data processing coordinator with specialized processors.
    
    Integrates specialized processors for different data types while
    maintaining the core caching and configuration functionality.
    """
    
    def __init__(self):
        self._config = {}
        self._cache = {}
        
        # Initialize specialized processors
        self.histogram = HistogramProcessor()
        self.copy_numbers = CopyNumberProcessor()
        self.transitions = TransitionProcessor()
    
    def configure(self,
                 simulation_dirs: List[str],
                 simulations: Optional[List[int]] = None,
                 species: Optional[List[str]] = None,
                 time_frame: Optional[Tuple[float, float]] = None,
                 cache_dir: Optional[str] = None):
        """Configure data processing parameters."""
        self._config = {
            'simulation_dirs': simulation_dirs,
            'simulations': simulations or list(range(len(simulation_dirs))),
            'species': species,
            'time_frame': time_frame,
            'cache_dir': cache_dir
        }
        self._selected_dirs = [simulation_dirs[i] for i in self._config['simulations']]
        self.histogram.configure(self._selected_dirs)
        self.copy_numbers.configure(self._selected_dirs)
        self.transitions.configure(self._selected_dirs)
    
    def get_histogram_data(self, **kwargs) -> Dict[str, Any]:
        """
        Get histogram complex data from multiple simulation directories.
        
        Parameters:
            sim_dirs (List[str]): List of simulation directories
            
        Returns:
            Dict[str, Any]:
                {
                    'raw_data': all data read,
                    'time_series': time series,
                    'species_filter': selected species,
                    'metadata': {
                        'num_simulations': number of simulations,
                        'time_frame': selected time frame,
                        'cache_key': cache_key
                }
        }
        """
        cache_key = self._generate_cache_key('histogram', **kwargs)
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Load raw data
        all_data = self.histogram.read_multiple(self._selected_dirs, self._config)
        
        # Process and structure data
        result = {
            'raw_data': all_data,
            'time_series': align_time_series(all_data),
            'species_filter': self._config['species'],
            'metadata': {
                'num_simulations': len(all_data),
                'time_frame': self._config['time_frame'],
                'cache_key': cache_key
            }
        }
        
        self._cache[cache_key] = result
        return result
    
    # def get_copy_numbers_data(self, **kwargs) -> Dict[str, Any]:
    #     """Get processed copy numbers data with enhanced processing."""
    #     cache_key = self._generate_cache_key('copy_numbers', **kwargs)
        
    #     if cache_key in self._cache:
    #         return self._cache[cache_key]
        
    #     # Load raw data
    #     dataframes = []
    #     for sim_dir in self._selected_dirs:
    #         df = self._data_io.get_copy_numbers(sim_dir)
    #         if df is not None:
    #             dataframes.append(df)
        
    #     # Process data
    #     result = {
    #         'dataframes': dataframes,
    #         'aligned_data': self.copy_numbers.align_time_series({'dataframes': dataframes}),
    #         'species_filter': self._config['species'],
    #         'metadata': {
    #             'num_simulations': len(dataframes),
    #             'cache_key': cache_key
    #         }
    #     }
        
    #     self._cache[cache_key] = result
    #     return result
    
    # def get_transition_data(self, **kwargs) -> Dict[str, Any]:
    #     """Get processed transition matrix and lifetime data."""
    #     cache_key = self._generate_cache_key('transition', **kwargs)
        
    #     if cache_key in self._cache:
    #         return self._cache[cache_key]
        
    #     # Load raw data
    #     matrices = []
    #     lifetimes = []
    #     for sim_dir in self._selected_dirs:
    #         matrix, lifetime = self._data_io.get_transition_matrix(sim_dir, self._config['time_frame'])
    #         if matrix is not None:
    #             matrices.append(matrix)
    #             lifetimes.append(lifetime)
        
    #     result = {
    #         'matrices': matrices,
    #         'lifetimes': lifetimes,
    #         'aggregated_matrix': self.transitions.aggregate_matrices({'matrices': matrices}),
    #         'metadata': {
    #             'num_simulations': len(matrices),
    #             'time_frame': self._config['time_frame'],
    #             'cache_key': cache_key
    #         }
    #     }
        
    #     self._cache[cache_key] = result
    #     return result
    
    # # Enhanced methods using processors
    # def get_time_series_statistics(self, legends: List[List[str]], **kwargs):
    #     """Get time series statistics for multiple legends."""
    #     histogram_data = self.get_histogram_data(**kwargs)
    #     return self.histogram.calculate_time_series_statistics(histogram_data, legends)

    # def get_complex_sizes(self, legend: List[str], **kwargs) -> List[List[int]]:
    #     """Extract complex sizes using histogram processor."""
    #     histogram_data = self.get_histogram_data(**kwargs)
    #     return self.histogram.calculate_complex_sizes(histogram_data, legend)
    
    # def get_size_distribution_stats(self, legend: List[str], **kwargs) -> Dict[str, float]:
    #     """Get statistical measures of complex size distribution."""
    #     histogram_data = self.get_histogram_data(**kwargs)
    #     return self.histogram.get_size_distribution_stats(histogram_data, legend)
    
    # def get_species_trends(self, species_groups: List[List[str]], **kwargs) -> Dict[str, Dict[str, Any]]:
    #     """Get time series trends for species groups."""
    #     copy_data = self.get_copy_numbers_data(**kwargs)
    #     return self.copy_numbers.calculate_trends(copy_data, species_groups)
    
    # def get_equilibrium_analysis(self, species_groups: List[List[str]], **kwargs) -> Dict[str, Any]:
    #     """Get equilibrium analysis for species groups."""
    #     copy_data = self.get_copy_numbers_data(**kwargs)
        
    #     return {
    #         'equilibrium_periods': self.copy_numbers.find_equilibrium_points(copy_data, species_groups),
    #         'time_to_equilibrium': self.copy_numbers.calculate_time_to_equilibrium(copy_data, species_groups),
    #         'statistics': self.copy_numbers.compute_statistics(copy_data, species_groups)
    #     }
    
    # def get_free_energy_landscape(self, **kwargs) -> Dict[str, Any]:
    #     """Get free energy landscape from transition data."""
    #     transition_data = self.get_transition_data(**kwargs)
    #     return self.transitions.calculate_free_energy(transition_data)
    
    # def get_pathway_analysis(self, **kwargs) -> Dict[str, Any]:
    #     """Get comprehensive pathway analysis."""
    #     transition_data = self.get_transition_data(**kwargs)
        
    #     return {
    #         'association_probs': self.transitions.calculate_association_probabilities(transition_data),
    #         'dissociation_probs': self.transitions.calculate_dissociation_probabilities(transition_data),
    #         'growth_probs': self.transitions.calculate_growth_probabilities(transition_data),
    #         'dominant_pathways': self.transitions.find_dominant_pathways(transition_data),
    #         'pathway_flux': self.transitions.calculate_pathway_flux(transition_data)
    #     }
    
    # def get_lifetime_analysis(self, **kwargs) -> Dict[str, Any]:
    #     """Get comprehensive lifetime analysis."""
    #     transition_data = self.get_transition_data(**kwargs)
        
    #     return {
    #         'lifetime_stats': self.transitions.calculate_lifetime_statistics(transition_data),
    #         'aggregated_lifetimes': self.transitions.aggregate_lifetimes(transition_data)
    #     }
    
    # ============================================
    # Utility methods
    # ============================================
    def _generate_cache_key(self, data_type: str, **kwargs) -> str:
        """Generate unique cache key based on configuration and parameters."""
        key_data = {
            'data_type': data_type,
            'simulations': tuple(self._config['simulations']),
            'species': tuple(self._config['species']) if self._config['species'] else None,
            'time_frame': self._config['time_frame'],
            **kwargs
        }
        key_str = str(sorted(key_data.items()))
        return hashlib.md5(key_str.encode()).hexdigest()[:12]
    
    def clear_cache(self):
        """Clear all cached data and processor caches."""
        self._cache.clear()
        self.histogram.clear_cache()
        self.copy_numbers.clear_cache()
        self.transitions.clear_cache()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        return {
            'num_entries': len(self._cache),
            'cache_keys': list(self._cache.keys()),
            'memory_usage_mb': sum(len(pickle.dumps(v)) for v in self._cache.values()) / (1024*1024),
            'processors_available': ['histogram', 'copy_numbers', 'transitions']
        }