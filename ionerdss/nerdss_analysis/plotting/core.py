"""
Core plotting configuration and management for ionerdss analysis.
Provides centralized plotting interface with legacy compatibility.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, Any, Optional, Tuple, List

# Import all existing plotting functions for delegation
from .line_plots import (
    plot_line_speciescopy_vs_time, plot_line_maximum_assembly_size_vs_time,
    plot_line_average_assembly_size_vs_time, plot_line_fraction_of_monomers_assembled_vs_time,
    plot_complex_count_vs_time, plot_line_free_energy
)
from .histogram_plots import (
    plot_hist_complex_species_size, plot_hist_monomer_counts_vs_complex_size,
    plot_stackedhist_complex_species_size
)
from .heatmap_plots import (
    plot_heatmap_complex_species_size, plot_heatmap_monomer_counts_vs_complex_size,
    plot_heatmap_species_a_vs_species_b
)
from .three_d_plots import (
    plot_hist_complex_species_size_3d, plot_hist_monomer_counts_vs_complex_size_3d
)
from .probability_plots import (
    plot_line_symmetric_association_probability, plot_line_asymmetric_association_probability,
    plot_line_symmetric_dissociation_probability, plot_line_asymmetric_dissociation_probability,
    plot_line_growth_probability, plot_line_liftime
)


class PlotConfigure:
    """
    Central plotting configuration and execution class.
    
    Manages all plotting operations with consistent styling and configuration.
    Provides both new modular interface and legacy compatibility.
    """
    
    def __init__(self, save_dir: str):
        """
        Initialize plotting configuration.
        
        Parameters:
            save_dir (str): Directory for saving plots and data
        """
        self.save_dir = save_dir
        self._config = {
            'style': 'seaborn',
            'context': 'paper',
            'font_size': 12,
            'figure_size': (10, 6),
            'color_palette': 'deep',
            'save_format': 'svg',
            'dpi': 300
        }
        self._style_configured = False
    
    def configure(self, **kwargs):
        """
        Configure plotting style and appearance.
        
        Parameters:
            style (str): Base plotting style ('seaborn', 'matplotlib', etc.)
            context (str): Seaborn context ('paper', 'notebook', 'talk', 'poster')
            font_size (int): Base font size
            figure_size (Tuple[int, int]): Default figure size
            color_palette (str): Color scheme
            save_format (str): Output format ('svg', 'png', 'pdf')
            dpi (int): Resolution for raster formats
            **kwargs: Additional matplotlib/seaborn parameters
        """
        self._config.update(kwargs)
        self._style_configured = False
    
    def _apply_style(self):
        """Apply configured style settings."""
        if self._style_configured:
            return
        
        # Set seaborn style and context
        if self._config['style'] == 'seaborn':
            sns.set_style("ticks")
            sns.set_context(self._config['context'], rc={
                "font.size": self._config['font_size'],
                "axes.titlesize": self._config['font_size'],
                "axes.labelsize": self._config['font_size'],
                "xtick.labelsize": self._config['font_size'],
                "ytick.labelsize": self._config['font_size'],
                "legend.fontsize": self._config['font_size'],
                "font.family": "serif"
            })
            sns.set_palette(self._config['color_palette'])
        
        plt.rcParams['figure.figsize'] = self._config['figure_size']
        plt.rcParams['savefig.dpi'] = self._config['dpi']
        plt.rcParams['savefig.format'] = self._config['save_format']
        
        self._style_configured = True
    
    def _get_simulation_dirs(self, data: 'Data') -> List[str]:
        """Extract simulation directories from Data object."""
        return [data._config['simulation_dirs'][i] for i in data._config['simulations']]
    
    # Line plot methods
    def line_speciescopy_vs_time(self, data: 'Data', legend: List[List[str]], **kwargs):
        """Create species copy number vs time line plot."""
        self._apply_style()
        
        # Extract parameters
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'figure_size': kwargs.get('figure_size', self._config['figure_size']),
            'show_type': kwargs.get('show_type', 'both'),
            'user_file_name': kwargs.get('user_file_name', None)
        }
        
        return plot_line_speciescopy_vs_time(**params)
    
    def line_assembly_size_vs_time(self, data: 'Data', assembly_type: str = "maximum", 
                                 legend: List[str] = None, **kwargs):
        """Create assembly size vs time line plot."""
        self._apply_style()
        
        base_params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'simulations_dir': data._config['simulation_dirs'],
            'figure_size': kwargs.get('figure_size', self._config['figure_size']),
            'show_type': kwargs.get('show_type', 'both')
        }
        
        if assembly_type == "maximum":
            return plot_line_maximum_assembly_size_vs_time(legend=legend or [], **base_params)
        elif assembly_type == "average":
            return plot_line_average_assembly_size_vs_time(legend=legend or [], **base_params)
        elif assembly_type == "fraction":
            return plot_line_fraction_of_monomers_assembled_vs_time(legend=legend or [], **base_params)
        else:
            raise ValueError(f"Unknown assembly_type: {assembly_type}")
    
    def line_complex_count_vs_time(self, data: 'Data', target_complexes: List[str], **kwargs):
        """Create complex count vs time line plot."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'target_complexes': target_complexes,
            'simulations_dir': data._config['simulation_dirs'],
            'figure_size': kwargs.get('figure_size', self._config['figure_size']),
            'show_type': kwargs.get('show_type', 'both')
        }
        
        return plot_complex_count_vs_time(**params)
    
    def line_free_energy_vs_size(self, data: 'Data', **kwargs):
        """Create free energy vs cluster size line plot."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'simulations_dir': data._config['simulation_dirs'],
            'time_frame': kwargs.get('time_frame', data._config.get('time_frame')),
            'figure_size': kwargs.get('figure_size', self._config['figure_size']),
            'show_type': kwargs.get('show_type', 'both')
        }
        
        return plot_line_free_energy(**params)
    
    def line_probability_vs_size(self, data: 'Data', probability_type: str, 
                                legend: List[str] = None, **kwargs):
        """Create probability vs cluster size line plot."""
        self._apply_style()
        
        base_params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'simulations_dir': data._config['simulation_dirs'],
            'time_frame': kwargs.get('time_frame', data._config.get('time_frame')),
            'figure_size': kwargs.get('figure_size', self._config['figure_size']),
            'show_type': kwargs.get('show_type', 'both'),
            'legend': legend
        }
        
        if probability_type == "symmetric_association":
            return plot_line_symmetric_association_probability(**base_params)
        elif probability_type == "asymmetric_association":
            return plot_line_asymmetric_association_probability(**base_params)
        elif probability_type == "symmetric_dissociation":
            return plot_line_symmetric_dissociation_probability(**base_params)
        elif probability_type == "asymmetric_dissociation":
            return plot_line_asymmetric_dissociation_probability(**base_params)
        elif probability_type == "growth":
            return plot_line_growth_probability(**base_params)
        elif probability_type == "lifetime":
            return plot_line_liftime(**base_params)
        else:
            raise ValueError(f"Unknown probability_type: {probability_type}")
    
    # Histogram plot methods
    def histogram_complex_size(self, data: 'Data', legend: List[str], **kwargs):
        """Create complex size histogram."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'bins': kwargs.get('bins', 10),
            'time_frame': kwargs.get('time_frame', data._config.get('time_frame')),
            'frequency': kwargs.get('frequency', False),
            'normalize': kwargs.get('normalize', False),
            'show_type': kwargs.get('show_type', 'both'),
            'figure_size': kwargs.get('figure_size', self._config['figure_size'])
        }
        
        return plot_hist_complex_species_size(**params)
    
    def histogram_monomer_count(self, data: 'Data', legend: List[str], **kwargs):
        """Create monomer count histogram."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'bins': kwargs.get('bins', 10),
            'time_frame': kwargs.get('time_frame', data._config.get('time_frame')),
            'frequency': kwargs.get('frequency', False),
            'normalize': kwargs.get('normalize', False),
            'show_type': kwargs.get('show_type', 'both'),
            'figure_size': kwargs.get('figure_size', self._config['figure_size'])
        }
        
        return plot_hist_monomer_counts_vs_complex_size(**params)
    
    def histogram_stacked(self, data: 'Data', legend: List[str], **kwargs):
        """Create stacked histogram."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'bins': kwargs.get('bins', 10),
            'time_frame': kwargs.get('time_frame', data._config.get('time_frame')),
            'frequency': kwargs.get('frequency', False),
            'normalize': kwargs.get('normalize', False),
            'show_type': kwargs.get('show_type', 'both'),
            'figure_size': kwargs.get('figure_size', self._config['figure_size'])
        }
        
        return plot_stackedhist_complex_species_size(**params)
    
    # 3D plot methods
    def histogram_3d_complex_size(self, data: 'Data', legend: List[str], **kwargs):
        """Create 3D complex size histogram."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'bins': kwargs.get('bins', 10),
            'time_bins': kwargs.get('time_bins', 10),
            'frequency': kwargs.get('frequency', False),
            'normalize': kwargs.get('normalize', False),
            'figure_size': kwargs.get('figure_size', self._config['figure_size'])
        }
        
        return plot_hist_complex_species_size_3d(**params)
    
    def histogram_3d_monomer_count(self, data: 'Data', legend: List[str], **kwargs):
        """Create 3D monomer count histogram."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'bins': kwargs.get('bins', 10),
            'time_bins': kwargs.get('time_bins', 10),
            'frequency': kwargs.get('frequency', False),
            'normalize': kwargs.get('normalize', False),
            'figure_size': kwargs.get('figure_size', self._config['figure_size'])
        }
        
        return plot_hist_monomer_counts_vs_complex_size_3d(**params)
    
    # Heatmap methods
    def heatmap_complex_size_time(self, data: 'Data', legend: List[str], **kwargs):
        """Create complex size vs time heatmap."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'bins': kwargs.get('bins', 10),
            'time_bins': kwargs.get('time_bins', 10),
            'frequency': kwargs.get('frequency', False),
            'normalize': kwargs.get('normalize', False),
            'figure_size': kwargs.get('figure_size', self._config['figure_size'])
        }
        
        return plot_heatmap_complex_species_size(**params)
    
    def heatmap_monomer_count_time(self, data: 'Data', legend: List[str], **kwargs):
        """Create monomer count vs time heatmap."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'bins': kwargs.get('bins', 10),
            'time_bins': kwargs.get('time_bins', 10),
            'frequency': kwargs.get('frequency', False),
            'normalize': kwargs.get('normalize', False),
            'figure_size': kwargs.get('figure_size', self._config['figure_size'])
        }
        
        return plot_heatmap_monomer_counts_vs_complex_size(**params)
    
    def heatmap_species_correlation(self, data: 'Data', legend: List[str], **kwargs):
        """Create species A vs species B heatmap."""
        self._apply_style()
        
        params = {
            'save_dir': self.save_dir,
            'simulations_index': data._config['simulations'],
            'legend': legend,
            'simulations_dir': data._config['simulation_dirs'],
            'bins': kwargs.get('bins', 10),
            'time_bins': kwargs.get('time_bins', 10),
            'frequency': kwargs.get('frequency', False),
            'normalize': kwargs.get('normalize', False),
            'figure_size': kwargs.get('figure_size', self._config['figure_size'])
        }
        
        return plot_heatmap_species_a_vs_species_b(**params)
    
    # Utility methods
    def save_current_plot(self, filename: str, **kwargs):
        """Save current plot to file."""
        save_path = os.path.join(self.save_dir, "figure_plot_data", filename)
        format_type = kwargs.get('format', self._config['save_format'])
        dpi = kwargs.get('dpi', self._config['dpi'])
        
        plt.savefig(save_path, format=format_type, dpi=dpi, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    def show_plot(self):
        """Display current plot."""
        plt.show()
    
    def clear_plot(self):
        """Clear current plot."""
        plt.clf()
    
    def get_config(self) -> Dict[str, Any]:
        """Get current plotting configuration."""
        return self._config.copy()
    
    def reset_style(self):
        """Reset style configuration."""
        self._style_configured = False
        plt.rcdefaults()
        sns.reset_defaults()