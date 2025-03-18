import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_line_speciescopy_vs_time(
    save_dir: str,
    simulations_index: list,
    legend: list,
    show_type: str = "both",
    simulations_dir: list = None,
    figure_size: tuple = (10, 6)
):
    """
    Plot species copy number vs. time for selected simulations.

    Parameters:
        save_dir (str): The base directory where simulations are stored.
        simulations_index (list): Indices of the simulations to include.
        legend (list): Species or groups of species to plot.
            - [['A(A1!1).A(A1!1)']] → plot 'A(A1!1).A(A1!1)'
            - [['A(A1!1).A(A1!1)'], ['A(A2!1).A(A2!1)']] → plot two species separately
            - [['A(A1!1).A(A1!1)', 'A(A2!1).A(A2!1)']] → plot their sum
        show_type (str): Display mode, "both", "individuals", or "average".
        simulations_dir (list, optional): List of directories for each simulation.
        figure_size (tuple): Size of the plot figure.
    """
    # Ensure the save path for processed data exists
    plot_data_dir = os.path.join(save_dir, "figure_plot_data")
    os.makedirs(plot_data_dir, exist_ok=True)

    # Initialize lists to store data
    all_sim_data = []

    # Load and preprocess data
    for idx in simulations_index:
        sim_dir = os.path.join(simulations_dir[idx], "DATA")
        data_file = os.path.join(sim_dir, "copy_numbers_time.dat")

        if not os.path.exists(data_file):
            print(f"Warning: {data_file} not found, skipping simulation {idx}.")
            continue

        df = pd.read_csv(data_file)
        df.rename(columns=lambda x: x.strip(), inplace=True)  # Strip spaces from column names

        # Store time and species data
        all_sim_data.append(df)

    if not all_sim_data:
        print("No valid simulation data found.")
        return
    
    # Align data to the shortest time series
    min_length = min(len(df) for df in all_sim_data)
    all_sim_data = [df.iloc[:min_length] for df in all_sim_data]

    # Compute average and standard deviation
    time_values = all_sim_data[0]["Time (s)"].values
    species_data = {}

    for species_list in legend:
        species_key = "+".join(species_list)
        values = np.array([df[species_list].sum(axis=1).values for df in all_sim_data])

        species_data[species_key] = {
            "mean": values.mean(axis=0),
            "std": values.std(axis=0),
            "raw": values
        }

    # Save processed data
    for species, data in species_data.items():
        save_path = os.path.join(plot_data_dir, f"{species.replace('+', '_')}.csv")
        df_to_save = pd.DataFrame({
            "Time (s)": time_values,
            "Mean": data["mean"],
            "Std": data["std"]
        })
        df_to_save.to_csv(save_path, index=False)
        print(f"Processed data for {species} saved to {save_path}")
    
    # Plot results
    plt.figure(figsize=(10, 6))
    sns.set_style("ticks")
    
    for species, data in species_data.items():
        if show_type in {"individuals", "both"}:
            for i, sim_values in enumerate(data["raw"]):
                plt.plot(time_values, sim_values, alpha=0.3, linestyle="dashed", label=f"{species} (simulation {i})" if show_type == "both" else None)

        if show_type in {"average", "both"}:
            plt.plot(time_values, data["mean"], label=f"{species} (average)", linewidth=2)
            plt.fill_between(time_values, data["mean"] - data["std"], data["mean"] + data["std"], alpha=0.2)

    plt.xlabel("Time (s)")
    plt.ylabel("Copy Number")
    plt.legend()
    plt.tight_layout()
    
    # Save plot
    plot_path = os.path.join(plot_data_dir, "species_vs_time_plot.svg")
    plt.savefig(plot_path, format="svg")
    print(f"Plot saved to {plot_path}")
    plt.show()

    print(f"Plot saved to {plot_path}")
