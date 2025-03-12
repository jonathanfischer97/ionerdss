import os
import json
from typing import Dict, Any, List
from ..nerdss_model.model import Model

class Simulation:
    """Class for handling NERDSS simulation configurations and running simulations.

    Attributes:
        model (Model): The model associated with the simulation.
        work_dir (str): The working directory for the simulation.
    """
    
    def __init__(self, model: Model, work_dir: str) -> None:
        """Initializes the Simulation class.
        
        Args:
            model (Model): The model to be used in the simulation.
            work_dir (str): The working directory for the simulation.
        """
        if work_dir.startswith("~"):
            work_dir = os.path.expanduser(work_dir)
        self.work_dir = os.path.abspath(work_dir)
        os.makedirs(self.work_dir, exist_ok=True)
        print(f"Working directory set to: {work_dir}")

        self.model = model
        self.work_dir = work_dir

        self.generate_nerdss_input()

    def generate_nerdss_input(self) -> None:
        """Generates the NERDSS input files based on the model."""
        # create a directory `nerdss_input` in the working directory
        input_dir = os.path.join(self.work_dir, "nerdss_input")
        os.makedirs(input_dir, exist_ok=True)

        # remove existing files and folders in the input directory
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)

        for mol in self.model.molecule_types:
            mol_file = os.path.join(input_dir, f"{mol.name}.mol")
            with open(mol_file, "w") as f:
                f.write(f"Name = {mol.name}\n")
                f.write("isLipid = false\n")
                f.write("isImplicitLipid = false\n")
                f.write("checkOverlap = false\n")
                f.write("countTransition = false\n")
                f.write("transitionMatrixSize = 500\n")
                f.write("insideCompartment = false\n")
                f.write("outsideCompartment = false\n")
                f.write("mass = 1.0\n")
                f.write("\n")
                f.write("D = [10.00, 10.00, 10.00]\n\n")
                f.write("Dr = [0.1, 0.1, 0.1]\n\n")

                f.write("COM\t0.0000\t0.0000\t0.0000\n")
                
                for iface in mol.interfaces:
                    f.write(f"{iface.name}\t{iface.coord.x / 10:.6f}\t{iface.coord.y / 10:.6f}\t{iface.coord.z / 10:.6f}\n")
                
                f.write("\nbonds = {}\n".format(len(mol.interfaces)))
                for iface in mol.interfaces:
                    f.write(f"com {iface.name}\n")

        inp_file = os.path.join(self.work_dir, "nerdss_input", "parms.inp")
        with open(inp_file, "w") as f:
            f.write("start parameters\n")
            f.write("\tnItr = 1000000\n")
            f.write("\ttimeStep = 0.1\n")
            f.write("\ttimeWrite = 10000\n")
            f.write("\ttrajWrite = 100000\n")
            f.write("\tpdbWrite = 100000\n")
            f.write("\trestartWrite = 100000\n")
            f.write("\tcheckPoint = 100000\n")
            f.write("\ttransitionWrite = 100000\n")
            f.write("\tclusterOverlapCheck = false\n")
            f.write("\tscaleMaxDisplace = 100.0\n")
            f.write("\toverlapSepLimit = 0.1\n")
            f.write("end parameters\n\n")

            f.write("start boundaries\n")
            f.write("\tWaterBox = [1000.0, 1000.0, 1000.0]\n")
            f.write("\thasCompartment = false\n")
            f.write("\tcompartmentR = 0\n")
            f.write("\tcompartmentSiteD = 0\n")
            f.write("\tcompartmentSiteRho = 0\n")
            f.write("end boundaries\n\n")

            f.write("start molecules\n")
            for mol in self.model.molecule_types:
                f.write(f"\t{mol.name} : 100\n")
            f.write("end molecules\n\n")

            f.write("start reactions\n")
            for reaction in self.model.reactions:
                f.write(f"\t{reaction.name}\n")
                f.write("\t\tonRate3Dka = 1000.0\n")
                f.write("\t\toffRatekb = 0.0\n")
                f.write(f"\t\tsigma = {reaction.binding_radius}\n")
                f.write(f"\t\tnorm1 = {list(reaction.norm1)}\n")
                f.write(f"\t\tnorm2 = {list(reaction.norm2)}\n")
                f.write(f"\t\tassocAngles = [{', '.join(map(str, reaction.binding_angles))}]\n")
                f.write("\t\tlength3Dto2D = 2.0\n")
                f.write("\t\tbindRadSameCom = 1.5\n")
                f.write("\t\tloopCoopFactor = 1.0\n")
                f.write("\t\texcludeVolumeBound = False\n\n")
            f.write("end reactions\n")

    def modify_mol_file(self, mol_name: str, modifications: Dict[str, Any]) -> None:
        """Modifies the parameters of an existing .mol file.
        
        Args:
            mol_name (str): The name of the molecule to modify.
            modifications (Dict[str, Any]): A dictionary containing parameter modifications.
        
        Raises:
            FileNotFoundError: If the specified molecule file does not exist.
        """
        input_dir = os.path.join(self.work_dir, "nerdss_input")
        mol_file = os.path.join(input_dir, f"{mol_name}.mol")
        
        if not os.path.exists(mol_file):
            available_mols = [f.split(".mol")[0] for f in os.listdir(input_dir) if f.endswith(".mol")]
            raise FileNotFoundError(f"Molecule '{mol_name}' not found. Available molecules: {', '.join(available_mols)}")
        
        with open(mol_file, "r") as f:
            lines = f.readlines()
        
        with open(mol_file, "w") as f:
            for line in lines:
                key = line.split("=")[0].strip()
                if key in modifications:
                    f.write(f"{key} = {modifications[key]}\n")
                else:
                    f.write(line)

    def modify_inp_file(self, modifications: Dict[str, Any], filename: str = "parms.inp") -> None:
        """
        Modifies the parameters of the parms.inp file. If `isSphere` and `sphereR` are provided, 
        removes the `WaterBox` line and adds the new lines accordingly. If `WaterBox` is provided, 
        removes `isSphere` and `sphereR` if they exist.
        
        Args:
            modifications (Dict[str, Any]): A dictionary containing parameter modifications.
            filename (str): The name of the input file to modify. Defaults to "parms.inp".
        """
        inp_file = os.path.join(self.work_dir, "nerdss_input", filename)
        
        if not os.path.exists(inp_file):
            raise FileNotFoundError(f"{filename} file not found.")
        
        with open(inp_file, "r") as f:
            lines = f.readlines()
        
        modified_lines = []
        in_boundaries_section = False
        waterbox_removed = False
        sphere_removed = False
        in_molecules_section = False
        in_reactions_section = False
        current_reaction = None
        molecule_types = []

        for line in lines:
            stripped_line = line.strip()
            
            if stripped_line.startswith("start boundaries"):
                in_boundaries_section = True
                modified_lines.append(line)
                continue
            
            if stripped_line.startswith("end boundaries"):
                in_boundaries_section = False
                
                if "isSphere" in modifications and "sphereR" in modifications:
                    modified_lines.append(f"\tisSphere = {modifications['isSphere']}\n")
                    modified_lines.append(f"\tsphereR = {modifications['sphereR']}\n")
                elif "WaterBox" in modifications:
                    modified_lines.append(f"\tWaterBox = {modifications['WaterBox']}\n")
                
                modified_lines.append(line)
                continue
            
            if in_boundaries_section:
                if stripped_line.startswith("WaterBox") and "isSphere" in modifications and "sphereR" in modifications:
                    waterbox_removed = True
                    continue
                elif (stripped_line.startswith("isSphere") or stripped_line.startswith("sphereR")) and "WaterBox" in modifications:
                    sphere_removed = True
                    continue

            if stripped_line.startswith("start molecules"):
                in_molecules_section = True
                modified_lines.append(line)
                continue
            if stripped_line.startswith("end molecules"):
                in_molecules_section = False
                modified_lines.append(line)
                continue
            
            if stripped_line.startswith("start reactions"):
                in_reactions_section = True
                modified_lines.append(line)
                continue
            if stripped_line.startswith("end reactions"):
                in_reactions_section = False
                modified_lines.append(line)
                continue

            if in_molecules_section and ":" in stripped_line:
                mol_name, count = map(str.strip, stripped_line.split(":"))
                molecule_types.append(mol_name)
                if mol_name in modifications:
                    modified_lines.append(f"\t{mol_name} : {modifications[mol_name]}\n")
                else:
                    modified_lines.append(line)
                continue

            if in_reactions_section:
                if '=' not in stripped_line and stripped_line:
                    current_reaction = stripped_line.strip()
                    modified_lines.append(line)
                    continue
                if current_reaction and current_reaction in modifications:
                    param_name = stripped_line.split("=")[0].strip()
                    if param_name in modifications[current_reaction]:
                        modified_lines.append(f"\t\t{param_name} = {modifications[current_reaction][param_name]}\n")
                        continue
            
            key = stripped_line.split("=")[0].strip()
            if key in modifications:
                modified_lines.append(f"\t{key} = {modifications[key]}\n")
            else:
                modified_lines.append(line)
        
        with open(inp_file, "w") as f:
            f.writelines(modified_lines)

    def add_interface_state(self, mol_name: str, interface_name: str, states: List[str]) -> None:
        """Adds states to a specified interface of a molecule.
        
        Args:
            mol_name (str): The name of the molecule.
            interface_name (str): The name of the interface.
            states (List[str]): List of single-character state names.
        
        Raises:
            FileNotFoundError: If the molecule file does not exist.
            ValueError: If no valid states are provided.
        """
        if not states or any(len(state) != 1 for state in states):
            raise ValueError("States must be single-character values.")

        input_dir = os.path.join(self.work_dir, "nerdss_input")
        mol_file = os.path.join(input_dir, f"{mol_name}.mol")
        
        if not os.path.exists(mol_file):
            available_mols = [f.split(".mol")[0] for f in os.listdir(input_dir) if f.endswith(".mol")]
            raise FileNotFoundError(f"Molecule '{mol_name}' not found. Available molecules: {', '.join(available_mols)}")
        
        with open(mol_file, "a") as f:
            state_line = f"state = {interface_name}~" + "~".join(states) + "\n"
            f.write(state_line)

    def print_mol_parameters(self, mol_name: str) -> None:
        """Prints all parameters of a given .mol file.
        
        Args:
            mol_name (str): The name of the molecule to display.
        
        Raises:
            FileNotFoundError: If the specified molecule file does not exist.
        """
        input_dir = os.path.join(self.work_dir, "nerdss_input")
        mol_file = os.path.join(input_dir, f"{mol_name}.mol")
        
        if not os.path.exists(mol_file):
            available_mols = [f.split(".mol")[0] for f in os.listdir(input_dir) if f.endswith(".mol")]
            raise FileNotFoundError(f"Molecule '{mol_name}' not found. Available molecules: {', '.join(available_mols)}")
        
        with open(mol_file, "r") as f:
            print(f"Parameters for molecule '{mol_name}':")
            print(f.read())

    def print_inp_file(self, file_name: str = "parms.inp") -> None:
        """
        Prints the contents of the parms.inp file.
        
        Args:
            file_name (str): The name of the input file to print. Defaults to "parms.inp".
        """
        inp_file = os.path.join(self.work_dir, "nerdss_input", file_name)
        
        if not os.path.exists(inp_file):
            print("parms.inp file not found.")
            return
        
        with open(inp_file, "r") as f:
            print(f.read())

    def run_simulation(self) -> None:
        # Placeholder for running the actual NERDSS simulation
        pass
