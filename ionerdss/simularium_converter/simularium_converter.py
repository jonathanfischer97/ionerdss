# written by Hassan Sohail
import os
import glob
import re
import colorsys
import numpy as np

from simulariumio.nerdss import NerdssConverter, NerdssData
from simulariumio import MetaData, DisplayData, DISPLAY_TYPE, CameraData, UnitData
from simulariumio.filters import TranslateFilter
from simulariumio.writers import BinaryWriter

def parse_parms(filename):
    """
    Read a parms.inp file (full path) and return (pdb_write, water_box_list, time_step).
    """
    pdb_write = None
    time_step = None
    water_box = None

    with open(filename) as f:
        section = None
        for line in f:
            line = line.strip()
            if line == "start parameters":
                section = "parameters"
                continue
            elif line == "end parameters":
                section = None
            elif line == "start boundaries":
                section = "boundaries"
                continue
            elif line == "end boundaries":
                section = None

            if section == "parameters":
                if line.startswith("pdbWrite"):
                    pdb_write = int(line.split("=", 1)[1].strip())
                elif line.startswith("timeStep"):
                    time_step = float(line.split("=", 1)[1].strip())
            elif section == "boundaries" and line.startswith("WaterBox"):
                nums = re.search(r"\[([^\]]+)\]", line).group(1)
                water_box = [float(x) for x in nums.split(",")]

    return pdb_write, water_box, time_step


def parse_mol_file(fp):
    """
    Read a single .mol file (full path fp).
    Return (molecule_name, COM_array, {site_label: coord_array, ...}).
    """
    lines = [l.strip() for l in open(fp) if l.strip()]
    # Extract the "Name = ..." line
    name = next(l.split("=", 1)[1].strip() for l in lines if l.startswith("Name"))

    coords = {}
    started = False
    for l in lines:
        t = l.split()
        if len(t) == 4:
            try:
                coords[t[0]] = np.array(list(map(float, t[1:])))
                started = True
            except ValueError:
                # skip lines that aren’t numeric
                pass
        elif started:
            # once numeric block ends, stop
            break

    com = coords.pop("COM")
    return name, com, coords


def compute_avg_distance(com, sites):
    """
    Given a COM array and a dict of {site: coord_array}, return the average
    Euclidean distance from COM to each site. If no sites, return 0.
    """
    if not sites:
        return 0
    return np.mean([np.linalg.norm(coord - com) for coord in sites.values()])


def generate_distinct_colors(n):
    """
    Return a list of n distinct hex‐color strings by sampling HSV space.
    """
    colors = []
    for i in range(n):
        rgb = colorsys.hsv_to_rgb(i / n, 0.7, 0.9)
        rgb_255 = [int(channel * 255) for channel in rgb]
        colors.append("#{0:02X}{1:02X}{2:02X}".format(*rgb_255))
    return colors


def parse_sigmas(fp):
    """
    Read reactions/“sigma” lines from a .inp file (full path fp).
    Return dict keyed by (molecule_name, site_label) → sigma_scaled_float.
    """
    m = {}
    with open(fp) as f:
        in_rx = False
        sites = []
        for l in f:
            l = l.strip()
            if l.startswith("start reactions"):
                in_rx = True
                continue
            if l.startswith("end reactions"):
                break
            if not in_rx:
                continue

            if "<->" in l:
                # capture all Molecule(Site) occurrences
                sites = re.findall(r"([A-Za-z0-9_]+)\(([A-Za-z0-9_]+)\)", l)
            elif l.startswith("sigma"):
                s = float(l.split("=", 1)[1].strip())
                for mol, site in sites:
                    m[(mol, site)] = s * 0.6
    return m


def build_display_data(input_dir):
    """
    In input_dir, find all .mol and one .inp, then build a dict of DisplayData
    keyed by "Molecule#Site" or "Molecule#COM".
    """
    # Patterns for files
    mol_pattern = os.path.join(input_dir, "*.mol")
    inp_pattern = os.path.join(input_dir, "*.inp")

    mol_files = sorted(glob.glob(mol_pattern))
    inp_files = sorted(glob.glob(inp_pattern))

    if not mol_files:
        raise FileNotFoundError(f"No .mol files found in '{input_dir}'")
    if not inp_files:
        raise FileNotFoundError(f"No .inp file found in '{input_dir}'")
    if len(inp_files) > 1:
        raise FileExistsError(f"Multiple .inp files found in '{input_dir}': {inp_files}")

    params_file = inp_files[0]

    # Parse each .mol
    parsed = [parse_mol_file(fp) for fp in mol_files]
    names = [item[0] for item in parsed]
    colors = generate_distinct_colors(len(names))
    cmap = dict(zip(names, colors))

    # Pull in any explicit sigma values
    sigmas = parse_sigmas(params_file)

    display_dict = {}
    mol_sigmas = {}

    # Create a DisplayData for each site
    for name, com, sites in parsed:
        for site_label, coord in sites.items():
            key = f"{name}#{site_label}"
            radius = sigmas.get((name, site_label), compute_avg_distance(com, sites) * 0.3)
            display_dict[key] = DisplayData(
                name=f"{name}-{site_label}",
                display_type=DISPLAY_TYPE.SPHERE,
                radius=radius,
                color=cmap[name],
            )
            mol_sigmas.setdefault(name, []).append(radius)

    # Now make a COM sphere for each molecule
    for name, com, sites in parsed:
        radii = mol_sigmas.get(name, [1.0])
        avg_radius = sum(radii) / len(radii)
        key_com = f"{name}#COM"
        display_dict[key_com] = DisplayData(
            name=f"{name}-COM",
            display_type=DISPLAY_TYPE.SPHERE,
            radius=avg_radius,
            color=cmap[name],
        )

    return display_dict


def convert_simularium(input_dir: str, output_name: str, pdb_folder: str = '') -> None:
    """
    Given a directory `input_dir` containing:
      - parms.inp
      - one or more .mol files
      - a subfolder "PDB/" with PDB trajectory files
    this function will read everything, build display data, center the coordinates,
    and write out `output_name.simularium` in the current working directory.

    Raises FileNotFoundError or FileExistsError if those files/folders are missing.
    """
    # 1) Verify input_dir exists
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Input folder '{input_dir}' does not exist.")

    # 2) Check for PDB subfolder
    if pdb_folder == '':
        pdb_folder = os.path.join(input_dir, "PDB")
    if not os.path.isdir(pdb_folder):
        raise FileNotFoundError(f"Expected subfolder 'PDB' in '{input_dir}', but not found.")

    # 3) Parse parms.inp
    parms_path = os.path.join(input_dir, "parms.inp")
    if not os.path.isfile(parms_path):
        raise FileNotFoundError(f"'parms.inp' not found in '{input_dir}'.")

    pdb_write, water_box, time_step = parse_parms(parms_path)
    if water_box is None or time_step is None:
        raise RuntimeError("Could not parse WaterBox or timeStep from parms.inp.")

    box_array = np.array(water_box, dtype=float)

    # 4) Build the dictionary of DisplayData from the .mol files
    display_data = build_display_data(input_dir)

    # 5) Construct a NerdssData object
    nerdss_data = NerdssData(
        path_to_pdb_files=pdb_folder,
        meta_data=MetaData(
            box_size=box_array,
            trajectory_title=output_name,
            camera_defaults=CameraData(position=np.array([0, 0, box_array[2] / 2])),
        ),
        display_data=display_data,
        time_units=UnitData("µs", time_step),
        spatial_units=UnitData("nm", 1),
    )

    # 6) Center everything in the box
    converter = NerdssConverter(nerdss_data)
    translate_filter = TranslateFilter(default_translation=box_array / -2)
    filtered_data = converter.filter_data([translate_filter])

    # 7) Write a binary .simularium file
    BinaryWriter.save(filtered_data, output_name, False)
    # After this, a file named f"{output_name}.simularium" appears in cwd.
