import os
import seaborn as sns

from .plot_figures import (
    plot_line_speciescopy_vs_time,
    plot_line_maximum_assembly_size_vs_time,)

class Analysis:
    def __init__(self, save_dir: str = None):
        # Resolve the directory path
        if save_dir is None:
            save_dir = os.getcwd()
        elif save_dir.startswith("~"):
            save_dir = os.path.expanduser(save_dir)

        self.save_dir = os.path.abspath(save_dir)

        # Determine if it's a single simulation or a batch
        if os.path.exists(os.path.join(self.save_dir, "DATA")):
            self.simulation_dirs = [self.save_dir]
            print("Detected a single simulation directory.")
        else:
            # Find parent directories containing a "DATA" folder
            self.simulation_dirs = [
                root for root, dirs, _ in os.walk(self.save_dir) if "DATA" in dirs
            ]
            print(f"Detected a batch of {len(self.simulation_dirs)} simulation directories.")

    def plot_figure(
        self,
        figure_type: str = "line",
        simulations: list = None,
        x: str = "time",
        y: str = "species",
        z: str = None,
        legend: list = None,
        show_type: str = "both",
        font_size: int = 12,
        figure_size: tuple = (10, 6),
        seaborn_style: str = "ticks",
        seaborn_context: str = "paper",
    ):
        """
        Plot a figure based on the specified type and data.

        Parameters:
            figure_type (str): Type of figure to plot. Options are:
                - "line" (line plot)
                - "hist" (histogram)
                - "3dhist" (3D histogram)
                - "heatmap" (heatmap)
            
            simulations (list, optional): List of index of simulation directories to include in the plot.
                If None, uses all available simulations.
            
            x (str): Variable for the x-axis.
            y (str): Variable for the y-axis.
            z (str, optional): Variable for the z-axis (only used in "3dhist" and "heatmap").
            
            legend (list, optional): Labels for the legend. If None, uses default labels.
            
            show_type (str): Determines what data to display. Options are:
                - "individuals" → Shows all individual simulation results.
                - "average" → Shows only the averaged result.
                - "both" → Shows both individual and average results.

            font_size (int): Font size for the plot.
            figure_size (tuple): Size of the figure in inches.
            seaborn_style (str): Seaborn style for the plot. Default is "ticks".
                Options include "white", "dark", "whitegrid", "darkgrid", and "ticks".
            seaborn_context (str): Seaborn context for the plot. Default is "paper".
                Options include "paper", "notebook", "talk", and "poster".

        Raises:
            ValueError: If `figure_type` or `show_type` is invalid.
        """

        sns.set_style(seaborn_style)
        sns.set_context(seaborn_context, rc={
            "font.size": font_size,
            "axes.titlesize": font_size,
            "axes.labelsize": font_size,
            "xtick.labelsize": font_size,
            "ytick.labelsize": font_size,
            "legend.fontsize": font_size,
            "font.family": "serif"
        })
        
        valid_figure_types = {"line", "hist", "3dhist", "heatmap"}
        valid_show_types = {"both", "individuals", "average"}

        if figure_type not in valid_figure_types:
            raise ValueError(f"Invalid figure_type '{figure_type}'. Must be one of {valid_figure_types}.")

        if show_type not in valid_show_types:
            raise ValueError(f"Invalid show_type '{show_type}'. Must be one of {valid_show_types}.")

        simulations = simulations or []
        if not simulations:
            print("No simulations specified. Using all available simulations.")
            for i, sim_dir in enumerate(self.simulation_dirs):
                simulations.append(i)
        legend = legend or []
        if not legend:
            raise ValueError("Legend must be provided.")

        # Placeholder for actual plotting logic
        print(f"Plotting {figure_type} with:")
        print(f"- x-axis: {x}")
        print(f"- y-axis: {y}")
        print(f"- z-axis: {z if z else 'None'}")
        print(f"- Simulations: {len(simulations)} selected")
        print(f"- Legend: {legend if legend else 'None'}")
        print(f"- Display mode: {show_type}")

        if figure_type == "line" and x == "time" and y == "species":
            plot_line_speciescopy_vs_time(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )

        if figure_type == "line" and x == "time" and y == "maximum_assembly":
            plot_line_maximum_assembly_size_vs_time(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )