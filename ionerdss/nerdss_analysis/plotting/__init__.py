"""
Plotting module for ionerdss analysis.
Provides both new modular interface and legacy compatibility.
"""

# Import new plotting core
from .core import PlotConfigure

# Import all existing plotting functions for backward compatibility
from .line_plots import (
    plot_line_speciescopy_vs_time,
    plot_line_maximum_assembly_size_vs_time,
    plot_line_average_assembly_size_vs_time,
    plot_line_fraction_of_monomers_assembled_vs_time,
    plot_complex_count_vs_time,
    plot_line_free_energy
)

from .histogram_plots import (
    plot_hist_complex_species_size,
    plot_hist_monomer_counts_vs_complex_size,
    plot_stackedhist_complex_species_size,
    plot_hist_complex_species_size_3d,
    plot_hist_monomer_counts_vs_complex_size_3d
)

from .heatmap_plots import (
    plot_heatmap_complex_species_size,
    plot_heatmap_monomer_counts_vs_complex_size,
    plot_heatmap_species_a_vs_species_b
)

from .three_d_plots import (
    plot_hist_complex_species_size_3d as plot_3d_hist_complex_species_size,
    plot_hist_monomer_counts_vs_complex_size_3d as plot_3d_hist_monomer_species
)

from .probability_plots import (
    plot_line_symmetric_association_probability,
    plot_line_asymmetric_association_probability,
    plot_line_symmetric_dissociation_probability,
    plot_line_asymmetric_dissociation_probability,
    plot_line_growth_probability,
    plot_line_liftime
)

__version__ = "2.0.0"

# New API exports
__all__ = ["PlotConfigure"]

# Legacy function exports for backward compatibility
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
    "plot_hist_complex_species_size_3d",
    "plot_hist_monomer_counts_vs_complex_size_3d",
    
    # Heatmap plots
    "plot_heatmap_complex_species_size",
    "plot_heatmap_monomer_counts_vs_complex_size", 
    "plot_heatmap_species_a_vs_species_b",
    
    # 3D plots
    "plot_3d_hist_complex_species_size",
    "plot_3d_hist_monomer_species",
    
    # Probability plots
    "plot_line_symmetric_association_probability",
    "plot_line_asymmetric_association_probability",
    "plot_line_symmetric_dissociation_probability",
    "plot_line_asymmetric_dissociation_probability",
    "plot_line_growth_probability",
    "plot_line_liftime",
])