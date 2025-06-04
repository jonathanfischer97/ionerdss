"""
ionerdss.nerdss_analysis package - Enhanced analysis tools for NERDSS simulations.

This package provides comprehensive tools for analyzing and visualizing NERDSS 
simulation results with both modern modular API and legacy compatibility.

Main Classes:
    Analysis: Primary interface for simulation analysis and visualization
    Data: Advanced data processing with specialized processors  
    PlotConfigure: Centralized plotting configuration and execution

Usage:
    # New modular API (recommended)
    import ionerdss as ion
    analysis = ion.Analysis("/path/to/simulations")
    data = analysis.get_data(simulations=[0,1,2], species=["A","B"])
    plot = analysis.set_plot(figure_size=(12,8))
    plot.line_speciescopy_vs_time(data=data, legend=[["A"], ["B"]])
    
    # Legacy API (backward compatible)
    analysis = ion.Analysis("/path/to/simulations") 
    analysis.plot_figure(figure_type="line", x="time", y="species", 
                        legend=[["A"], ["B"]], simulations=[0,1,2])
"""

# Main interface
from .analysis import Analysis

# Core components for advanced usage
from .data import Data
from .plotting import PlotConfigure

# Legacy plotting functions for backward compatibility
from .plotting import (
    # Line plots
    plot_line_speciescopy_vs_time,
    plot_line_maximum_assembly_size_vs_time,
    plot_line_average_assembly_size_vs_time, 
    plot_line_fraction_of_monomers_assembled_vs_time,
    plot_complex_count_vs_time,
    plot_line_free_energy,
    
    # Histogram plots
    plot_hist_complex_species_size,
    plot_hist_monomer_counts_vs_complex_size,
    plot_stackedhist_complex_species_size,
    
    # Heatmap plots  
    plot_heatmap_complex_species_size,
    plot_heatmap_monomer_counts_vs_complex_size,
    plot_heatmap_species_a_vs_species_b,
    
    # 3D plots
    plot_hist_complex_species_size_3d,
    plot_hist_monomer_counts_vs_complex_size_3d,
    
    # Probability plots
    plot_line_symmetric_association_probability,
    plot_line_asymmetric_association_probability,
    plot_line_symmetric_dissociation_probability,
    plot_line_asymmetric_dissociation_probability,
    plot_line_growth_probability,
    plot_line_liftime,
)

# Legacy imports for complete backward compatibility
from .plot_figures import *

__version__ = "2.0.0"
__author__ = "ionerdss development team"

# Primary exports - most users only need Analysis
__all__ = ["Analysis"]

# Advanced API exports for power users
__all__.extend(["Data", "PlotConfigure"])

# Legacy function exports for existing code
__all__.extend([
    # Line plots
    "plot_line_speciescopy_vs_time",
    "plot_line_maximum_assembly_size_vs_time",
    "plot_line_average_assembly_size_vs_time", 
    "plot_line_fraction_of_monomers_assembled_vs_time",
    "plot_complex_count_vs_time",
    "plot_line_free_energy",
    
    # Histogram plots
    "plot_hist_complex_species_size", 
    "plot_hist_monomer_counts_vs_complex_size",
    "plot_stackedhist_complex_species_size",
    
    # Heatmap plots
    "plot_heatmap_complex_species_size",
    "plot_heatmap_monomer_counts_vs_complex_size",
    "plot_heatmap_species_a_vs_species_b",
    
    # 3D plots
    "plot_hist_complex_species_size_3d",
    "plot_hist_monomer_counts_vs_complex_size_3d",
    
    # Probability plots  
    "plot_line_symmetric_association_probability",
    "plot_line_asymmetric_association_probability",
    "plot_line_symmetric_dissociation_probability", 
    "plot_line_asymmetric_dissociation_probability",
    "plot_line_growth_probability",
    "plot_line_liftime",
])

def get_version():
    """Get package version."""
    return __version__

def get_help():
    """Get basic usage help."""
    help_text = """
ionerdss.nerdss_analysis - NERDSS Simulation Analysis Tools

Quick Start:
-----------
# Import the package
import ionerdss as ion

# Initialize analysis 
analysis = ion.Analysis("/path/to/simulation/directory")

# New modular API (recommended):
data = analysis.get_data(simulations=[0,1,2])  # Select simulations
plot = analysis.set_plot(figure_size=(12,8))   # Configure plotting
plot.line_speciescopy_vs_time(data=data, legend=[["A"], ["B"]])

# Legacy API (backward compatible):
analysis.plot_figure(figure_type="line", x="time", y="species", 
                    legend=[["A"], ["B"]], simulations=[0,1,2])

# Advanced data processing:
histogram_data = data.get_histogram_data()
size_stats = data.get_size_distribution_stats(legend=["A", "B"])
free_energy = data.get_free_energy_landscape()

For detailed documentation, see individual class and method docstrings.
    """
    return help_text.strip()

# Convenience function for quick analysis
def quick_analysis(simulation_dir: str, **kwargs):
    """
    Quick analysis setup for common use cases.
    
    Parameters:
        simulation_dir (str): Path to simulation directory
        **kwargs: Additional Analysis initialization parameters
        
    Returns:
        Analysis: Configured Analysis object
        
    Example:
        analysis = ion.quick_analysis("/path/to/sims")
        analysis.plot_figure(figure_type="line", x="time", y="species", legend=[["A"]])
    """
    return Analysis(simulation_dir, **kwargs)