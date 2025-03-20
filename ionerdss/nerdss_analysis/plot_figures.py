import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

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

def plot_line_maximum_assembly_size_vs_time(
    save_dir: str,
    simulations_index: list,
    legend: list,
    show_type: str = "both",
    simulations_dir: list = None,
    figure_size: tuple = (10, 6)
):
    """
    Plot the maximum assembly size vs. time based on species composition in complexes.

    Parameters:
        save_dir (str): The base directory where simulations are stored.
        simulations_index (list): Indices of the simulations to include.
        legend (list): Species to consider in assembly size calculation.
        show_type (str): Display mode, "both", "individuals", or "average".
        simulations_dir (list): List of simulation directories.
        figure_size (tuple): Size of the figure.
    """

    plot_data_dir = os.path.join(save_dir, "figure_plot_data")
    os.makedirs(plot_data_dir, exist_ok=True)

    all_sim_data = []

    for idx in simulations_index:
        sim_dir = os.path.join(simulations_dir[idx], "DATA")
        data_file = os.path.join(sim_dir, "histogram_complexes_time.dat")

        if not os.path.exists(data_file):
            print(f"Warning: {data_file} not found, skipping simulation {idx}.")
            continue

        time_series = []
        max_assembly_sizes = []

        with open(data_file, "r") as f:
            lines = f.readlines()

        current_time = None
        current_complexes = []

        for line in lines:
            time_match = re.match(r"Time \(s\): (\d*\.?\d+)", line)
            if time_match:
                if current_time is not None:
                    # Process previous time block
                    max_size = max([sum(complex_dict.values()) for complex_dict in current_complexes], default=0)
                    time_series.append(current_time)
                    max_assembly_sizes.append(max_size)
                    current_complexes = []

                current_time = float(time_match.group(1))
            else:
                match = re.match(r"(\d+)\s+([\w\.\s:]+)", line)
                if match:
                    count = int(match.group(1))
                    species_data = match.group(2).split()
                    species_dict = {}

                    for i in range(0, len(species_data), 2):
                        species_name = species_data[i].strip(":")
                        species_count = float(species_data[i + 1].strip("."))

                        if species_name in legend:
                            species_dict[species_name] = species_dict.get(species_name, 0) + species_count

                    if species_dict:
                        total_size = sum(species_dict.values())
                        current_complexes.extend([species_dict] * count)

        if current_time is not None:
            max_size = max([sum(complex_dict.values()) for complex_dict in current_complexes], default=0)
            time_series.append(current_time)
            max_assembly_sizes.append(max_size)

        if time_series and max_assembly_sizes:
            df = pd.DataFrame({"Time (s)": time_series, "Max Assembly Size": max_assembly_sizes})
            all_sim_data.append(df)

    if not all_sim_data:
        print("No valid simulation data found.")
        return

    min_length = min(len(df) for df in all_sim_data)
    all_sim_data = [df.iloc[:min_length] for df in all_sim_data]

    time_values = all_sim_data[0]["Time (s)"].values
    max_sizes = np.array([df["Max Assembly Size"].values for df in all_sim_data])

    avg_max_size = max_sizes.mean(axis=0)
    std_max_size = max_sizes.std(axis=0)

    save_path = os.path.join(plot_data_dir, "max_assembly_size_vs_time.csv")
    df_to_save = pd.DataFrame({
        "Time (s)": time_values,
        "Mean Max Assembly Size": avg_max_size,
        "Std Max Assembly Size": std_max_size
    })
    df_to_save.to_csv(save_path, index=False)

    print(f"Processed data saved to {save_path}")

    plt.figure(figsize=figure_size)

    if show_type in {"individuals", "both"}:
        for i, sim_values in enumerate(max_sizes):
            plt.plot(time_values, sim_values, alpha=0.3, linestyle="dashed", label=f"Individual run {i}" if show_type == "both" else None)

    if show_type in {"average", "both"}:
        plt.plot(time_values, avg_max_size, label="Average", linewidth=2)
        plt.fill_between(time_values, avg_max_size - std_max_size, avg_max_size + std_max_size, alpha=0.2)

    plt.xlabel("Time (s)")
    plt.ylabel("Max Assembly Size")
    plt.legend()
    plt.tight_layout()

    plot_path = os.path.join(plot_data_dir, "max_assembly_size_vs_time.svg")
    plt.savefig(plot_path, format="svg")
    plt.show()

    print(f"Plot saved to {plot_path}")

def parse_complex_line(line):
    """Parse a single complex line and return a dictionary with species and counts."""
    match = re.match(r"(\d+)\s+([\w\.\s:]+)", line)
    if not match:
        return None, None

    count = int(match.group(1))  # Number of such complexes
    species_data = match.group(2).split()  # Split species and counts
    species_dict = {}

    for i in range(0, len(species_data), 2):
        species_name = species_data[i].strip(":")
        species_count = float(species_data[i + 1].strip("."))

        species_dict[species_name] = species_dict.get(species_name, 0) + species_count

    return count, species_dict

def compute_average_assembly_size(complexes, conditions):
    """
    Compute the average assembly size for given conditions.

    Parameters:
        complexes (list): List of tuples (count, species_dict) representing each complex.
        conditions (list): List of conditions, e.g., ["A>=2", "A+B>=4"].

    Returns:
        dict: Condition -> average assembly size mapping.
    """
    results = {}

    for condition in conditions:
        species_conditions = condition.split(", ")  # Handle multiple species constraints
        numerator, denominator = 0, 0

        for count, species_dict in complexes:
            valid = True
            total_size = 0

            for cond in species_conditions:
                species_match = re.match(r"(\w+)([>=<]=?|==)(\d+)", cond)
                if not species_match:
                    continue  # Skip invalid conditions

                species, operator, threshold = species_match.groups()
                threshold = int(threshold)
                species_count = species_dict.get(species, 0)

                if operator == ">=" and species_count < threshold:
                    valid = False
                elif operator == ">" and species_count <= threshold:
                    valid = False
                elif operator == "<=" and species_count > threshold:
                    valid = False
                elif operator == "<" and species_count >= threshold:
                    valid = False
                elif operator == "==" and species_count != threshold:
                    valid = False

                total_size += species_count  # Sum the species count

            if valid:
                numerator += count * total_size
                denominator += count

        results[condition] = numerator / denominator if denominator > 0 else 0

    return results

def plot_line_average_assembly_size_vs_time(
    save_dir: str,
    simulations_index: list,
    legend: list,
    show_type: str = "both",
    simulations_dir: list = None,
    figure_size: tuple = (10, 6)
):
    """
    Plot the average assembly size vs. time based on species composition in complexes.

    Parameters:
        save_dir (str): The base directory where simulations are stored.
        simulations_index (list): Indices of the simulations to include.
        legend (list): Conditions for computing average assembly size.
        show_type (str): Display mode, "both", "individuals", or "average".
        simulations_dir (list): List of simulation directories.
        figure_size (tuple): Size of the figure.
    """

    plot_data_dir = os.path.join(save_dir, "figure_plot_data")
    os.makedirs(plot_data_dir, exist_ok=True)

    all_sim_data = []

    for idx in simulations_index:
        sim_dir = os.path.join(simulations_dir[idx], "DATA")
        data_file = os.path.join(sim_dir, "histogram_complexes_time.dat")

        if not os.path.exists(data_file):
            print(f"Warning: {data_file} not found, skipping simulation {idx}.")
            continue

        time_series = []
        condition_results = {condition: [] for condition in legend}

        with open(data_file, "r") as f:
            lines = f.readlines()

        current_time = None
        current_complexes = []

        for line in lines:
            time_match = re.match(r"Time \(s\): (\d*\.?\d+)", line)
            if time_match:
                if current_time is not None:
                    # Compute average size for the previous time step
                    avg_sizes = compute_average_assembly_size(current_complexes, legend)
                    for cond in legend:
                        condition_results[cond].append(avg_sizes.get(cond, 0))

                    time_series.append(current_time)
                    current_complexes = []

                current_time = float(time_match.group(1))
            else:
                count, species_dict = parse_complex_line(line)
                if species_dict:
                    current_complexes.append((count, species_dict))

        if current_time is not None:
            avg_sizes = compute_average_assembly_size(current_complexes, legend)
            for cond in legend:
                condition_results[cond].append(avg_sizes.get(cond, 0))
            time_series.append(current_time)

        if time_series:
            df = pd.DataFrame({"Time (s)": time_series, **condition_results})
            all_sim_data.append(df)

    if not all_sim_data:
        print("No valid simulation data found.")
        return

    # Align data to the shortest time series
    min_length = min(len(df) for df in all_sim_data)
    all_sim_data = [df.iloc[:min_length] for df in all_sim_data]

    time_values = all_sim_data[0]["Time (s)"].values
    avg_data = {cond: np.array([df[cond].values for df in all_sim_data]) for cond in legend}

    # Compute mean and standard deviation
    mean_values = {cond: data.mean(axis=0) for cond, data in avg_data.items()}
    std_values = {cond: data.std(axis=0) for cond, data in avg_data.items()}

    # Save processed data
    save_path = os.path.join(plot_data_dir, "average_assembly_size_vs_time.csv")
    df_to_save = pd.DataFrame({"Time (s)": time_values, **{f"Mean {cond}": mean_values[cond] for cond in legend},
                               **{f"Std {cond}": std_values[cond] for cond in legend}})
    df_to_save.to_csv(save_path, index=False)
    print(f"Processed data saved to {save_path}")

    # Plot the data
    plt.figure(figsize=figure_size)
    sns.set_style("ticks")

    for cond in legend:
        if show_type in {"individuals", "both"}:
            for i, sim_values in enumerate(avg_data[cond]):
                plt.plot(time_values, sim_values, alpha=0.3, linestyle="dashed",
                         label=f"Individual run {i} ({cond})" if show_type == "both" else None)

        if show_type in {"average", "both"}:
            plt.plot(time_values, mean_values[cond], label=f"Average ({cond})", linewidth=2)
            plt.fill_between(time_values, mean_values[cond] - std_values[cond], mean_values[cond] + std_values[cond], alpha=0.2)

    plt.xlabel("Time (s)")
    plt.ylabel("Average Assembly Size")
    plt.legend()
    plt.tight_layout()

    plot_path = os.path.join(plot_data_dir, "average_assembly_size_vs_time.svg")
    plt.savefig(plot_path, format="svg")
    plt.show()

    print(f"Plot saved to {plot_path}")

def plot_line_fraction_of_monomers_assembled_vs_time(
    save_dir: str,
    simulations_index: list,
    legend: list,
    show_type: str = "both",
    simulations_dir: list = None,
    figure_size: tuple = (10, 6)
):
    """
    Plot the fraction of monomers assembled in complex vs. time based on species composition in complexes.
    
    Parameters:
        save_dir (str): The base directory where simulations are stored.
        simulations_index (list): Indices of the simulations to include.
        legend (list): Conditions for computing assembly fractions (e.g., ["A>=2"]).
        show_type (str): Display mode, "both", "individuals", or "average".
        simulations_dir (list): List of simulation directories.
        figure_size (tuple): Size of the figure.
    """
    plot_data_dir = os.path.join(save_dir, "figure_plot_data")
    os.makedirs(plot_data_dir, exist_ok=True)
    
    all_sim_data = []
    
    for idx in simulations_index:
        sim_dir = os.path.join(simulations_dir[idx], "DATA")
        data_file = os.path.join(sim_dir, "histogram_complexes_time.dat")
        
        if not os.path.exists(data_file):
            print(f"Warning: {data_file} not found, skipping simulation {idx}.")
            continue
        
        time_series = []
        fraction_results = {condition: [] for condition in legend}
        
        with open(data_file, "r") as f:
            lines = f.readlines()
        
        current_time = None
        current_complexes = []
        
        for line in lines:
            time_match = re.match(r"Time \(s\): (\d*\.?\d+)", line)
            if time_match:
                if current_time is not None:
                    for cond in legend:
                        selected_counts = 0
                        total_counts = 0

                        for count, complex_dict in current_complexes:
                            matches, target_species = eval_condition(complex_dict, cond)

                            if matches:
                                selected_counts += count * complex_dict.get(target_species, 0)  # Sum only the target species count

                            if target_species in complex_dict:
                                total_counts += count * complex_dict[target_species]  # Sum only in complexes where species exists

                        fraction = selected_counts / total_counts if total_counts > 0 else 0
                        fraction_results[cond].append(fraction)

                    time_series.append(current_time)
                    current_complexes = []

                current_time = float(time_match.group(1))
            else:
                count, species_dict = parse_complex_line(line)
                if species_dict:
                    current_complexes.append((count, species_dict))

        if current_time is not None:
            for cond in legend:
                selected_counts = 0
                total_counts = 0

                for count, complex_dict in current_complexes:
                    matches, target_species = eval_condition(complex_dict, cond)

                    if matches:
                        selected_counts += count * complex_dict.get(target_species, 0)  # Sum only the target species count

                    if target_species in complex_dict:
                        total_counts += count * complex_dict[target_species]  # Sum only in complexes where species exists

                fraction = selected_counts / total_counts if total_counts > 0 else 0
                fraction_results[cond].append(fraction)

            time_series.append(current_time)

        if time_series:
            df = pd.DataFrame({"Time (s)": time_series, **fraction_results})
            all_sim_data.append(df)
    
    if not all_sim_data:
        print("No valid simulation data found.")
        return
    
    min_length = min(len(df) for df in all_sim_data)
    all_sim_data = [df.iloc[:min_length] for df in all_sim_data]
    
    time_values = all_sim_data[0]["Time (s)"].values
    fraction_data = {cond: np.array([df[cond].values for df in all_sim_data]) for cond in legend}
    
    mean_values = {cond: data.mean(axis=0) for cond, data in fraction_data.items()}
    std_values = {cond: data.std(axis=0) for cond, data in fraction_data.items()}
    
    save_path = os.path.join(plot_data_dir, "fraction_of_monomers_assembled_vs_time.csv")
    df_to_save = pd.DataFrame({"Time (s)": time_values, **{f"Mean {cond}": mean_values[cond] for cond in legend},
                               **{f"Std {cond}": std_values[cond] for cond in legend}})
    df_to_save.to_csv(save_path, index=False)
    print(f"Processed data saved to {save_path}")
    
    plt.figure(figsize=figure_size)
    sns.set_style("ticks")
    
    for cond in legend:
        if show_type in {"individuals", "both"}:
            for i, sim_values in enumerate(fraction_data[cond]):
                plt.plot(time_values, sim_values, alpha=0.3, linestyle="dashed",
                         label=f"Individual run {i} ({cond})" if show_type == "both" else None)
        
        if show_type in {"average", "both"}:
            plt.plot(time_values, mean_values[cond], label=f"Average ({cond})", linewidth=2)
            plt.fill_between(time_values, mean_values[cond] - std_values[cond], mean_values[cond] + std_values[cond], alpha=0.2)
    
    plt.xlabel("Time (s)")
    plt.ylabel("Fraction of Monomers Assembled")
    plt.legend()
    plt.tight_layout()
    
    plot_path = os.path.join(plot_data_dir, "fraction_of_monomers_assembled_vs_time.svg")
    plt.savefig(plot_path, format="svg")
    plt.show()
    
    print(f"Plot saved to {plot_path}")

def eval_condition(species_dict, condition):
    """
    Evaluates whether a complex meets a condition based on species count.
    
    Parameters:
        species_dict (dict): Dictionary containing species counts in one complex.
        condition (str): A condition string like "B>=3".
    
    Returns:
        bool: True if the complex satisfies the condition, otherwise False.
    """
    species_match = re.match(r"(\w+)([>=<]=?|==)(\d+)", condition)
    if not species_match:
        return False

    species, operator, threshold = species_match.groups()
    threshold = int(threshold)
    
    species_count = species_dict.get(species, 0)  # Get count for the species
    return eval(f"{species_count} {operator} {threshold}"), species

def plot_hist_complex_species_size(
    save_dir: str,
    simulations_index: list,
    legend: list,
    bins: int = 10,
    time_frame: tuple = None,
    frequency: bool = False,
    normalize: bool = False,
    show_type: str = "both",
    simulations_dir: list = None,
    figure_size: tuple = (10, 6)
):
    """
    Plot a histogram of the average number or frequency of different complex species sizes over a time frame.
    The X-axis represents complex species size (only considering species in the legend), and the Y-axis 
    represents the average count or frequency, optionally normalized.

    Parameters:
        save_dir (str): The base directory where simulation results are stored.
        simulations_index (list): Indices of the simulations to include.
        legend (list): Species to be counted in determining complex sizes.
        bins (int): Number of bins for the histogram.
        time_frame (tuple, optional): Time range (start, end) to consider for averaging.
        frequency (bool): Whether to plot frequency instead of absolute count.
        normalize (bool): Whether to normalize the histogram (ensuring total area = 1).
        show_type (str): Display mode - "both", "individuals", or "average".
        simulations_dir (list): List of directories for each simulation.
        figure_size (tuple): Size of the figure.
    """
    plot_data_dir = os.path.join(save_dir, "figure_plot_data")
    os.makedirs(plot_data_dir, exist_ok=True)
    
    all_sizes_per_sim = []
    all_sizes_combined = []

    # Step 1: Collect all sizes across simulations
    for idx in simulations_index:
        sim_dir = os.path.join(simulations_dir[idx], "DATA")
        data_file = os.path.join(sim_dir, "histogram_complexes_time.dat")
        
        if not os.path.exists(data_file):
            print(f"Warning: {data_file} not found, skipping simulation {idx}.")
            continue
        
        with open(data_file, "r") as f:
            lines = f.readlines()
        
        current_time = None
        sim_sizes = []

        for line in lines:
            time_match = re.match(r"Time \(s\): (\d*\.?\d+)", line)
            if time_match:
                current_time = float(time_match.group(1))
                if time_frame and (current_time <= time_frame[0] or current_time >= time_frame[1]):
                    continue
            else:
                count, species_dict = parse_complex_line(line)
                if species_dict:
                    complex_size = sum(species_dict[species] for species in legend if species in species_dict)
                    sim_sizes.extend([complex_size] * count)

        if sim_sizes:
            all_sizes_per_sim.append(sim_sizes)
            all_sizes_combined.extend(sim_sizes)  # Accumulate sizes for global binning

    if not all_sizes_per_sim:
        print("No valid simulation data found.")
        return
    
    # Step 2: Determine global bin edges
    global_hist, bin_edges = np.histogram(all_sizes_combined, bins=bins)  # Global bin edges
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = bin_edges[1] - bin_edges[0]

    # print out bin edges and bin centers for debugging
    print(f"Bin edges: {bin_edges}")
    print(f"Bin centers: {bin_centers}")
    
    # Step 3: Compute histograms for each simulation using the same bin edges
    hist_values_all = []

    for sizes in all_sizes_per_sim:
        hist_values, _ = np.histogram(sizes, bins=bin_edges)  # Use fixed bin_edges
        hist_values_all.append(hist_values)

    hist_values_all = np.array(hist_values_all)

    # Step 4: Compute mean and standard deviation
    mean_values = np.mean(hist_values_all, axis=0)
    std_values = np.std(hist_values_all, axis=0)

    total = np.sum(mean_values)
    
    if frequency and total > 0:
        mean_values = mean_values / total
        std_values = std_values / total
    
    if normalize and total > 0:
        mean_values = mean_values / bin_width
        std_values = std_values / bin_width

    # Save data
    df_to_save = pd.DataFrame({
        "Bin Center": bin_centers,
        "Mean Count": mean_values,
        "Std Dev": std_values
    })
    save_path = os.path.join(plot_data_dir, "hist_average_number_vs_size.csv")
    df_to_save.to_csv(save_path, index=False)
    print(f"Processed data saved to {save_path}")

    # Step 5: Plot with error bars
    plt.figure(figsize=figure_size)
    plt.bar(bin_centers, mean_values, width=bin_width * 0.9, alpha=0.7, label="Mean")
    plt.errorbar(bin_centers, mean_values, yerr=std_values, fmt='o', color='black', capsize=5, label="Std Dev")

    species_all = "+".join(legend)
    plt.xlabel(f"Number of {species_all} in Complexes")
    plt.ylabel("Normalized Frequency" if normalize else ("Frequency" if frequency else "Complex Count"))
    plt.legend()
    plt.tight_layout()

    plot_path = os.path.join(plot_data_dir, "hist_average_number_vs_size.svg")
    plt.savefig(plot_path, format="svg")
    plt.show()
    
    print(f"Plot saved to {plot_path}")
