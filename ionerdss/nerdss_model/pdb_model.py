"""PDBModel module for generating NERDSS molecule types and reactions from a PDB structure.

This module defines the `PDBModel` class, which extends the `Model` class to generate NERDSS molecule types,
reactions, and corresponding files from a PDB structure.
"""

import gzip
import os
import requests
import numpy as np
from Bio.PDB import PDBList, MMCIFParser, PDBParser
from Bio.PDB.Polypeptide import is_aa
from scipy.spatial import KDTree
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from .model import Model, Coords


class PDBModel(Model):
    """Handles the generation of NERDSS molecule types and reactions from a PDB structure.

    Attributes:
        pdb_file (str): Path to the PDB structure file.
        pdb_id (str): PDB ID of the structure.
        save_dir (str): Directory to save the output files.
    """

    def __init__(self, pdb_file: str = None, pdb_id: str = None, save_dir: str = None):
        """Initializes a PDBModel object.

        Args:
            pdb_file (str, optional): Path to the PDB structure file. Defaults to None.
            pdb_id (str, optional): PDB ID of the structure. Defaults to None.
            save_dir (str, optional): Directory to save output files. Defaults to None.

        Raises:
            ValueError: If neither `pdb_file` nor `pdb_id` is provided.
        """
        if save_dir.startswith("~"):
            save_dir = os.path.expanduser(save_dir)
        super().__init__(save_dir)
        self.pdb_file = pdb_file
        self.pdb_id = pdb_id
        self.save_dir = os.path.abspath(save_dir) if save_dir else os.getcwd()

        if not self.pdb_file and not self.pdb_id:
            raise ValueError("Either 'pdb_file' or 'pdb_id' must be provided.")

        if not self.pdb_file:
            self.pdb_file = self.download_pdb()

        self.all_atoms_structure = self.pdb_parser()

        self.all_chains = []
        self.all_COM_chains_coords = []
        self.all_interfaces = []
        self.all_interfaces_coords = []
        self.all_interfaces_residues = []

    def download_pdb(self) -> str:
        """Downloads the PDB structure file.

        Returns:
            str: Path to the downloaded PDB file.

        Raises:
            ValueError: If the PDB ID is invalid or the file cannot be retrieved.
        """
        if not self.pdb_id or len(self.pdb_id) != 4:
            raise ValueError("Invalid PDB ID. PDB IDs must be four characters long.")

        pdb_id_upper = self.pdb_id.upper()
        pdb_id_lower = self.pdb_id.lower()
        assembly_url = f"https://files.rcsb.org/download/{pdb_id_upper}-assembly1.cif.gz"
        compressed_file = os.path.join(self.save_dir, f"{pdb_id_lower}-assembly1.cif.gz")
        decompressed_file = os.path.join(self.save_dir, f"{pdb_id_lower}.cif")

        try:
            response = requests.get(assembly_url, stream=True)
            if response.status_code == 200:
                with open(compressed_file, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Successfully downloaded assembly file: {compressed_file}")

                with gzip.open(compressed_file, 'rb') as f_in:
                    with open(decompressed_file, 'wb') as f_out:
                        f_out.write(f_in.read())
                return decompressed_file
            else:
                print(f"Assembly file not available for {pdb_id_upper} (status code: {response.status_code})")
        except requests.RequestException as e:
            print(f"Failed to download assembly file for {pdb_id_upper}: {e}")

        try:
            print(f"Downloading the CIF file for {pdb_id_upper}...")
            pdbl = PDBList()
            pdbl.retrieve_pdb_file(pdb_id_upper, pdir=self.save_dir, file_format="mmCif")
            return decompressed_file
        except Exception as e:
            raise ValueError(f"Failed to download PDB file for {pdb_id_upper}: {e}")


    def pdb_parser(self):
        """Parses the .cif or .pdb file into a Biopython Structure object.

        Returns:
            Bio.PDB.Structure.Structure: The parsed structure containing all atoms.

        Raises:
            ValueError: If the file format is not .cif or .pdb.
        """
        if self.pdb_file.endswith('.cif'):
            parser = MMCIFParser(QUIET=True)
        elif self.pdb_file.endswith('.pdb'):
            parser = PDBParser(QUIET=True)
        else:
            raise ValueError("Unsupported file format. Only .cif and .pdb files are supported.")

        structure_id = os.path.basename(self.pdb_file).split('.')[0]
        structure = parser.get_structure(structure_id, self.pdb_file)
        return structure

    def coarse_grain(self, distance_cutoff=0.35, residue_cutoff=3, show_coarse_grained_structure=False, save_pymol_script=False, standard_output=False):
        """Coarse grains the PDB structure by detecting binding interfaces between chains based on atomic distances.

        Args:
            distance_cutoff (float, optional): Max distance (nm) for atoms to be considered in contact. Defaults to 0.35.
            residue_cutoff (int, optional): Minimum residue pair count to be considered a valid interface. Defaults to 3.
            show_coarse_grained_structure (bool, optional): Whether to visualize the coarse-grained structure. Defaults to False.
            save_pymol_script (bool, optional): Whether to save a PyMOL script for visualization. Defaults to False.
            standard_output (bool, optional): Whether to print detected interfaces. Defaults to False.
        """
        self.all_chains = list(self.all_atoms_structure.get_chains())
        self.all_COM_chains_coords = []
        self.all_interfaces = []
        self.all_interfaces_coords = []
        self.all_interfaces_residues = []

        # Initialize interface lists
        num_chains = len(self.all_chains)
        for _ in range(num_chains):
            self.all_interfaces.append([])
            self.all_interfaces_coords.append([])
            self.all_interfaces_residues.append([])

        # Calculate the center of mass (COM) for each chain
        for chain in self.all_chains:
            atom_coords = [atom.coord for residue in chain for atom in residue if is_aa(residue)]
            if not atom_coords:
                self.all_COM_chains_coords.append(None)
                continue

            # Calculate the COM
            avg_coords = np.mean(atom_coords, axis=0)
            self.all_COM_chains_coords.append(Coords(*avg_coords))

        # Helper function to compute bounding box for a chain
        def compute_bounding_box(chain):
            atom_coords = np.array([atom.coord for residue in chain for atom in residue if is_aa(residue)])
            if atom_coords.size == 0:
                return None, None
            min_coords = np.min(atom_coords, axis=0)
            max_coords = np.max(atom_coords, axis=0)
            return min_coords, max_coords
        
        # Precompute bounding boxes for all chains
        bounding_boxes = [compute_bounding_box(chain) for chain in self.all_chains]

        # Helper function to process a pair of chains
        def process_chain_pair(i, j):
            if self.all_COM_chains_coords[i] is None or self.all_COM_chains_coords[j] is None:
                return

            min_box1, max_box1 = bounding_boxes[i]
            min_box2, max_box2 = bounding_boxes[j]

            # Skip if bounding boxes are farther apart than the cutoff distance
            if np.any(min_box2 > max_box1 + distance_cutoff * 10) or np.any(max_box2 < min_box1 - distance_cutoff * 10):
                return
            
            chain1 = self.all_chains[i]
            chain2 = self.all_chains[j]

            atom_coords_chain1 = []
            ca_coords_chain1 = []
            residue_ids_chain1 = []
            atom_coords_chain2 = []
            ca_coords_chain2 = []
            residue_ids_chain2 = []

            for residue1 in chain1:
                if not is_aa(residue1) or 'CA' not in residue1:
                    continue
                for atom1 in residue1:
                    atom_coords_chain1.append(atom1.coord)
                    ca_coords_chain1.append(residue1['CA'].coord)
                    residue_ids_chain1.append(residue1.id[1])

            for residue2 in chain2:
                if not is_aa(residue2) or 'CA' not in residue2:
                    continue
                for atom2 in residue2:
                    atom_coords_chain2.append(atom2.coord)
                    ca_coords_chain2.append(residue2['CA'].coord)
                    residue_ids_chain2.append(residue2.id[1])

            if len(ca_coords_chain1) == 0 or len(ca_coords_chain2) == 0:
                return

            # Build KDTree for chain2
            tree = KDTree(atom_coords_chain2)
            indices = tree.query_ball_point(atom_coords_chain1, r=distance_cutoff * 10)

            interface1 = []
            interface1_coords = []
            interface2 = []
            interface2_coords = []

            # Collect interface residues based on KDTree results
            for idx1, neighbors in enumerate(indices):
                if neighbors:
                    if residue_ids_chain1[idx1] not in interface1:
                        interface1.append(residue_ids_chain1[idx1])
                        interface1_coords.append(ca_coords_chain1[idx1])

                    for idx2 in neighbors:
                        if residue_ids_chain2[idx2] not in interface2:
                            interface2.append(residue_ids_chain2[idx2])
                            interface2_coords.append(ca_coords_chain2[idx2])

            # Store results if any interfaces were found
            if len(interface1) >= residue_cutoff and len(interface2) >= residue_cutoff:
                avg_coords1 = np.mean(interface1_coords, axis=0)
                self.all_interfaces[i].append(self.all_chains[j].id)
                self.all_interfaces_coords[i].append(Coords(*avg_coords1))
                self.all_interfaces_residues[i].append(interface1)
                avg_coords2 = np.mean(interface2_coords, axis=0)
                self.all_interfaces[j].append(self.all_chains[i].id)
                self.all_interfaces_coords[j].append(Coords(*avg_coords2))
                self.all_interfaces_residues[j].append(interface2)

        # Parallelize chain pair processing
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_chain_pair, i, j) for i in range(num_chains - 1) for j in range(i + 1, num_chains)]
            for future in futures:
                future.result()  # Wait for all tasks to complete

        # Print detected interfaces
        if standard_output:
            print("Binding interfaces detected:")
            for i, chain in enumerate(self.all_chains):
                print(f"Chain {chain.id}:")
                print(f"  Center of Mass (COM): {self.all_COM_chains_coords[i]}")
                print(f"  Interfaces: {self.all_interfaces[i]}")
                print("  Interface Coordinates: ")
                for interface_coord in self.all_interfaces_coords[i]:
                    print(f"    {interface_coord}")

        # Save PyMOL script
        if save_pymol_script:
            self.save_original_coarse_grained_structure()

        # Plot the original coarse-grained structure
        if show_coarse_grained_structure:
            self.plot_original_coarse_grained_structure()

    def plot_original_coarse_grained_structure(self):
        """Visualizes the original coarse-grained structure, showing each chain’s COM and interface coordinates before regularization."""
        all_points = []
        chain_ids = []
        for chain in self.all_chains:
            chain_id = chain.id
            chain_ids.append(chain_id)
            com_coord = self.all_COM_chains_coords[self.all_chains.index([chain for chain in self.all_chains if chain.id == chain_id][0])]
            interface_coords = self.all_interfaces_coords[self.all_chains.index([chain for chain in self.all_chains if chain.id == chain_id][0])]
            points = []
            points.append([com_coord.x, com_coord.y, com_coord.z])
            for interface_coord in interface_coords:
                points.append([interface_coord.x, interface_coord.y, interface_coord.z])
            all_points.append(points)
        self.plot_points_3d(all_points, chain_ids)

    def plot_points_3d(self, points, chain_ids=None):
        """Plots sets of 3D points for multiple chains in a single 3D Matplotlib figure.

        Args:
            points (list): A list of arrays, each of shape (N, 3), representing a chain’s COM + interface sites.
            chain_ids (list, optional): A list of labels for each chain. Defaults to None.
        """

        # Prepare a 3D figure
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")

        # Generate a color cycle for different chains
        colors = plt.cm.get_cmap("tab10", len(points))

        for i, chain in enumerate(points):
            # chain[0] is the center of mass (COM)
            com = chain[0]
            # The remaining points in the chain are interface points
            interfaces = chain[1:]

            # Pick a color for this chain
            color = colors(i)

            # Plot the COM
            ax.scatter(com[0], com[1], com[2],
                    color=color,
                    s=70,  # size of marker
                    marker="o",
                    label=f"Chain {chain_ids[i]} COM" if chain_ids != None else None)

            # Plot interfaces and lines to the COM
            for j, interface in enumerate(interfaces):
                # Plot the interface point
                ax.scatter(interface[0], interface[1], interface[2],
                        color=color,
                        s=50,
                        marker="^")  # or any shape you like

                # Draw a line from the COM to this interface
                xs = [com[0], interface[0]]
                ys = [com[1], interface[1]]
                zs = [com[2], interface[2]]
                ax.plot(xs, ys, zs, color=color, linewidth=1)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Original Coarse-Grained Structure")

        ax.legend(loc="best")

        plt.tight_layout()
        plt.show()

    def save_original_coarse_grained_structure(self, output_cif: str = "original_coarse_grained_structure.cif", pymol_script: str = "original_visualize_coarse_grained.pml"):
        """Saves the original coarse-grained structure (COM and interface coordinates for each chain)
        to a CIF file and generates a PyMOL script for quick visualization.

        Args:
            output_cif (str, optional): Output .cif filename. Defaults to "original_coarse_grained_structure.cif".
            pymol_script (str, optional): Output .pml filename for PyMOL. Defaults to "original_visualize_coarse_grained.pml".
        """
        with open(output_cif, 'w') as cif_file:
            atom_id = 1

            # Write CIF header
            cif_file.write("# Coarse-grained structure CIF file\n")
            cif_file.write("data_coarse_grained\n")
            cif_file.write("_audit_conform_dict.text 'Original coarse-grained model generated by ionerdss'\n")
            cif_file.write("loop_\n")
            cif_file.write("_atom_site.group_PDB\n")
            cif_file.write("_atom_site.id\n")
            cif_file.write("_atom_site.label_atom_id\n")
            cif_file.write("_atom_site.label_comp_id\n")
            cif_file.write("_atom_site.label_asym_id\n")
            cif_file.write("_atom_site.Cartn_x\n")
            cif_file.write("_atom_site.Cartn_y\n")
            cif_file.write("_atom_site.Cartn_z\n")
            cif_file.write("_atom_site.occupancy\n")
            cif_file.write("_atom_site.B_iso_or_equiv\n")
            cif_file.write("_atom_site.type_symbol\n")

            # Write COM atoms for each chain
            for i, chain in enumerate(self.all_chains):
                if not self.all_COM_chains_coords[i]:
                    continue
                com = self.all_COM_chains_coords[i]
                cif_file.write(
                    f"ATOM  {atom_id:5d}  COM  MOL {chain.id}  "
                    f"{com.x:8.3f} {com.y:8.3f} {com.z:8.3f}  1.00  0.00  C\n"
                )
                atom_id += 1

                # Write interface atoms for the current chain
                for j, interface_coord in enumerate(self.all_interfaces_coords[i]):
                    cif_file.write(
                        f"ATOM  {atom_id:5d}  INT  MOL {chain.id}  "
                        f"{interface_coord.x:8.3f} {interface_coord.y:8.3f} {interface_coord.z:8.3f}  1.00  0.00  O\n"
                    )
                    atom_id += 1

        print(f"Coarse-grained structure saved to {output_cif}.")

        # Generate PyMOL script for visualization
        with open(pymol_script, 'w') as pml_file:
            pml_file.write("# PyMOL script to visualize coarse-grained structure\n")
            pml_file.write(f"load {output_cif}, coarse_grained\n")
            pml_file.write("hide everything\n")
            pml_file.write("show spheres, name COM\n")
            pml_file.write("show spheres, name INT\n")
            pml_file.write("set sphere_scale, 1.0\n")
            pml_file.write("color red, name COM\n")
            pml_file.write("color blue, name INT\n")
            
            # Create pseudo-atoms for COM and interfaces and draw lines
            atom_index = 1
            for i, chain in enumerate(self.all_chains):
                com = self.all_COM_chains_coords[i]
                if not com:
                    continue
                # Make a pseudoatom for the chain's COM
                pml_file.write(
                    f"pseudoatom com_{chain.id}, pos=[{com.x:.3f}, {com.y:.3f}, {com.z:.3f}], color=red\n"
                )
                
                # For each interface, create a pseudoatom and connect it to the COM
                for j, interface_coord in enumerate(self.all_interfaces_coords[i], start=1):
                    pml_file.write(
                        f"pseudoatom int_{chain.id}_{j}, pos=[{interface_coord.x:.3f}, "
                        f"{interface_coord.y:.3f}, {interface_coord.z:.3f}], color=blue\n"
                    )
                    # Use f-strings so {atom_index} is replaced numerically
                    pml_file.write(f"distance line{atom_index}, com_{chain.id}, int_{chain.id}_{j}\n")
                    pml_file.write(f"set dash_width, 4, line{atom_index}\n")
                    pml_file.write(f"set dash_gap, 0.5, line{atom_index}\n")
                    atom_index += 1

            pml_file.write("set sphere_transparency, 0.2\n")
            pml_file.write("bg_color white\n")
            pml_file.write("zoom all\n")

        print(f"PyMOL script saved to {pymol_script}. Run 'pymol {pymol_script}' to visualize the coarse-grained structure.")

    def regularize_homo_chains(self):
        """Regularize homo chains to same nerdss molecule type."""
        pass
