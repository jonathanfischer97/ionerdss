"""
Transition matrix and lifetime data processor.
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict


class TransitionProcessor:
    """
    Specialized processor for transition matrix and lifetime data.
    
    Handles matrix operations, probability calculations,
    and lifetime statistics for cluster dynamics analysis.
    """
    
    def __init__(self):
        self._cache = {}
        self._selected_dirs = []

    def configure(self, selected_dirs: List[str]):
        self._selected_dirs = selected_dirs
    
    def aggregate_matrices(self, transition_data: Dict[str, Any]) -> np.ndarray:
        """Aggregate transition matrices across simulations."""
        matrices = transition_data['matrices']
        if not matrices:
            return np.array([])
        
        # Ensure all matrices have the same shape
        max_size = max(matrix.shape[0] for matrix in matrices)
        
        # Pad smaller matrices with zeros
        padded_matrices = []
        for matrix in matrices:
            if matrix.shape[0] < max_size:
                padded = np.zeros((max_size, max_size))
                padded[:matrix.shape[0], :matrix.shape[1]] = matrix
                padded_matrices.append(padded)
            else:
                padded_matrices.append(matrix)
        
        # Sum all matrices
        return np.sum(padded_matrices, axis=0)
    
    def calculate_size_probabilities(self, transition_data: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """Calculate probability distribution for each cluster size."""
        aggregated_matrix = self.aggregate_matrices(transition_data)
        if aggregated_matrix.size == 0:
            return {'probabilities': np.array([]), 'sizes': np.array([])}
        
        # Calculate total counts per size (sum over rows)
        counts_per_size = aggregated_matrix.sum(axis=1)
        total_counts = counts_per_size.sum()
        
        if total_counts == 0:
            probabilities = np.zeros_like(counts_per_size)
        else:
            probabilities = counts_per_size / total_counts
        
        sizes = np.arange(1, len(probabilities) + 1)
        
        return {
            'probabilities': probabilities,
            'sizes': sizes,
            'counts': counts_per_size,
            'total_counts': total_counts
        }
    
    def calculate_free_energy(self, transition_data: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """Calculate free energy landscape from size probabilities."""
        prob_data = self.calculate_size_probabilities(transition_data)
        probabilities = prob_data['probabilities']
        
        # Calculate free energy: F = -ln(P)
        with np.errstate(divide='ignore', invalid='ignore'):
            free_energy = -np.log(probabilities)
            free_energy[np.isinf(free_energy)] = np.nan
        
        return {
            'free_energy': free_energy,
            'sizes': prob_data['sizes'],
            'probabilities': probabilities
        }
    
    def calculate_association_probabilities(self, 
                                          transition_data: Dict[str, Any], 
                                          symmetric: bool = True) -> Dict[str, List[np.ndarray]]:
        """Calculate association probabilities for each cluster size."""
        aggregated_matrix = self.aggregate_matrices(transition_data)
        if aggregated_matrix.size == 0:
            return {'probabilities': [], 'sizes': np.array([])}
        
        max_size = aggregated_matrix.shape[0]
        association_probs = []
        
        for n in range(max_size - 1):
            assoc_counts = []
            
            for m in range(n + 1, max_size):
                pair_size = m - n
                count = aggregated_matrix[m, n]
                
                # For symmetric counting, divide by 2 when pair_size == n + 1
                if symmetric and pair_size == n + 1:
                    count /= 2
                    
                assoc_counts.append(count)
            
            total_assoc = sum(assoc_counts)
            if total_assoc > 0:
                probs = np.array(assoc_counts) / total_assoc
            else:
                probs = np.zeros(len(assoc_counts))
            
            association_probs.append(probs)
        
        return {
            'probabilities': association_probs,
            'sizes': np.arange(1, len(association_probs) + 1)
        }
    
    def calculate_dissociation_probabilities(self, 
                                           transition_data: Dict[str, Any], 
                                           symmetric: bool = True) -> Dict[str, List[np.ndarray]]:
        """Calculate dissociation probabilities for each cluster size."""
        aggregated_matrix = self.aggregate_matrices(transition_data)
        if aggregated_matrix.size == 0:
            return {'probabilities': [], 'sizes': np.array([])}
        
        max_size = aggregated_matrix.shape[0]
        dissociation_probs = []
        
        for n in range(1, max_size):
            dissoc_counts = []
            
            for m in range(n - 1, -1, -1):
                pair_size = n - m
                count = aggregated_matrix[m, n]
                
                # For symmetric counting, divide by 2 when pair_size == m + 1
                if symmetric and pair_size == m + 1:
                    count /= 2
                    
                dissoc_counts.append(count)
            
            total_dissoc = sum(dissoc_counts)
            if total_dissoc > 0:
                probs = np.array(dissoc_counts) / total_dissoc
            else:
                probs = np.zeros(len(dissoc_counts))
            
            dissociation_probs.append(probs)
        
        return {
            'probabilities': dissociation_probs,
            'sizes': np.arange(2, len(dissociation_probs) + 2)
        }
    
    def calculate_growth_probabilities(self, transition_data: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """Calculate growth vs shrinkage probabilities for each cluster size."""
        aggregated_matrix = self.aggregate_matrices(transition_data)
        if aggregated_matrix.size == 0:
            return {'growth_probs': np.array([]), 'sizes': np.array([])}
        
        max_size = aggregated_matrix.shape[0]
        growth_probs = []
        
        for n in range(max_size):
            # Count dissociation events (shrinkage)
            dissoc_counts = []
            for m in range(n - 1, -1, -1):
                pair_size = n - m
                count = aggregated_matrix[m, n]
                if pair_size == m + 1:
                    count /= 2
                dissoc_counts.append(count)
            
            # Count association events (growth)
            assoc_counts = []
            for m in range(n + 1, max_size):
                pair_size = m - n
                count = aggregated_matrix[m, n]
                if pair_size == n + 1:
                    count /= 2
                assoc_counts.append(count)
            
            total_dissoc = sum(dissoc_counts)
            total_assoc = sum(assoc_counts)
            total_events = total_dissoc + total_assoc
            
            if total_events > 0:
                growth_prob = total_assoc / total_events
            else:
                growth_prob = np.nan
            
            growth_probs.append(growth_prob)
        
        return {
            'growth_probs': np.array(growth_probs),
            'sizes': np.arange(1, len(growth_probs) + 1)
        }
    
    def aggregate_lifetimes(self, transition_data: Dict[str, Any]) -> Dict[int, List[float]]:
        """Aggregate lifetime data across simulations."""
        all_lifetimes = defaultdict(list)
        
        for lifetime_dict in transition_data['lifetimes']:
            for size, lifetimes in lifetime_dict.items():
                all_lifetimes[size].extend(lifetimes)
        
        return dict(all_lifetimes)
    
    def calculate_lifetime_statistics(self, transition_data: Dict[str, Any]) -> Dict[int, Dict[str, float]]:
        """Calculate statistical measures for lifetimes at each cluster size."""
        aggregated_lifetimes = self.aggregate_lifetimes(transition_data)
        
        lifetime_stats = {}
        for size, lifetimes in aggregated_lifetimes.items():
            if lifetimes:
                lifetime_array = np.array(lifetimes)
                lifetime_stats[size] = {
                    'mean': float(np.mean(lifetime_array)),
                    'std': float(np.std(lifetime_array)),
                    'median': float(np.median(lifetime_array)),
                    'min': float(np.min(lifetime_array)),
                    'max': float(np.max(lifetime_array)),
                    'count': len(lifetimes)
                }
            else:
                lifetime_stats[size] = {
                    'mean': 0.0, 'std': 0.0, 'median': 0.0,
                    'min': 0.0, 'max': 0.0, 'count': 0
                }
        
        return lifetime_stats
    
    def find_dominant_pathways(self, 
                             transition_data: Dict[str, Any], 
                             min_count: int = 10) -> List[Tuple[int, int, int]]:
        """Find dominant transition pathways (size_from, size_to, count)."""
        aggregated_matrix = self.aggregate_matrices(transition_data)
        if aggregated_matrix.size == 0:
            return []
        
        pathways = []
        rows, cols = np.where(aggregated_matrix >= min_count)
        
        for row, col in zip(rows, cols):
            count = int(aggregated_matrix[row, col])
            pathways.append((col + 1, row + 1, count))  # +1 for 1-based indexing
        
        # Sort by count (descending)
        pathways.sort(key=lambda x: x[2], reverse=True)
        
        return pathways
    
    def calculate_pathway_flux(self, transition_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate net flux for association vs dissociation pathways."""
        aggregated_matrix = self.aggregate_matrices(transition_data)
        if aggregated_matrix.size == 0:
            return {'association_flux': 0.0, 'dissociation_flux': 0.0, 'net_flux': 0.0}
        
        # Association flux: transitions to larger sizes
        assoc_flux = 0.0
        for i in range(aggregated_matrix.shape[0]):
            for j in range(i + 1, aggregated_matrix.shape[1]):
                assoc_flux += aggregated_matrix[j, i]
        
        # Dissociation flux: transitions to smaller sizes
        dissoc_flux = 0.0
        for i in range(aggregated_matrix.shape[0]):
            for j in range(i):
                dissoc_flux += aggregated_matrix[j, i]
        
        return {
            'association_flux': assoc_flux,
            'dissociation_flux': dissoc_flux,
            'net_flux': assoc_flux - dissoc_flux
        }
    
    def clear_cache(self):
        """Clear processor cache."""
        self._cache.clear()