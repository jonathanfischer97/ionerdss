"""Model module for generating NERDSS molecule types and reactions, and corresponding files.

This module defines the `Model` class, which serves as a container for molecule types,
reactions, and system parameters, along with associated helper classes.
`Model` class is the parent class for `PDBModel`, `DesignModel`, and `PlatonicSolidsModel` classes.
"""

import numpy as np
import os

class Model:
    """Parent class for all models to generate input files for NERDSS simulations.
    
    Attributes:
        path (str): Path to the saved NERDSS input files.
        molecule_types (list[MoleculeType]): List of molecule types.
        reactions (list[Reaction]): List of reactions.
        system_parameters (dict): Dictionary of system parameters.
        initial_molecule_counts (dict): Dictionary of initial molecule counts.
        system_geometry (dict): Dictionary of system geometry.
    """

    def __init__(self, path: str):
        """Initialize a Model object.

        Args:
            path (str): Path to the saved NERDSS input files.
        """
        self.path = os.path.abspath(path)
        # create the folder if it does not exist
        os.makedirs(self.path, exist_ok=True)

        self.molecule_types = []
        self.reactions = []
        self.system_parameters = {}
        self.initial_molecule_counts = {}
        self.system_geometry = {}

    def define_system_geometry(
        self,
        box_size: np.array = [1000, 1000, 1000],
        sphere_size: float = None,
        has_compartment: bool = False,
        compartment_site_d: float = 0.0,
        compartment_site_r: float = 0.0
    ):
        """Define system geometry.

        Args:
            box_size (np.array): Box size in x, y, and z directions. default = [1000, 1000, 1000]. unit: nm.
            sphere_size (np.array): Sphere radius. default = None. unit: nm.
            has_compartment (bool): Whether the system has a compartment. default = False.
            compartment_site_d (float): Compartment site diameter. default = 0.0. unit: nm^2/us.
            compartment_site_r (float): Compartment site radius. default = 0.0. unit: nm^-2.
        """
        self.system_geometry = {
            "box_size": box_size,
            "sphere_size": sphere_size,
            "has_compartment": has_compartment,
            "compartment_site_d": compartment_site_d,
            "compartment_site_r": compartment_site_r
        }

    def define_initial_molecule_counts(self, molecule_counts: dict):
        """Define initial molecule counts.

        Args:
            **kwargs: Initial molecule counts.
        """
        self.initial_molecule_counts = molecule_counts

    def define_system_parameters(
        self,
        n_itr: int = 10000000,
        time_step: float = 0.1,
        time_write: int = None,
        traj_write: int = None,
        restart_write: int = None,
        pdb_wreite: int = None,
        checkpoint_write: int = None,
        transition_write: int = None,
        cluster_overlap_check: bool = False,
        overlap_sep_limit: float = 0.1,
        scale_max_displace: float = 100.0,
    ):
        """Define system parameters.

        Args:
            n_itr (int): Number of iterations. default = 10000000.
            time_step (float): Time step in us. default = 0.1.
            time_write (int): Iteration interval to print running time information to standard output and to record the copy numbers in the _time.dat files. default = n_itr / 1000.
            traj_write (int): Trajectory write interval. default = n_itr / 100.
            restart_write (int): Restart write interval. default = n_itr / 100.
            pdb_wreite (int): PDB write interval. default = n_itr / 100.
            checkpoint_write (int): Checkpoint write interval. default = n_itr / 10.
            transition_write (int): Transition write interval. default = n_itr / 10.
            cluster_overlap_check (bool): Whether to check cluster overlap. default = False.
            overlap_sep_limit (float): Overlap separation limit. default = 0.1.
            scale_max_displace (float): Maximum displacement scale. default = 100.0.
        """
        if time_write is None:
            time_write = n_itr // 1000
        if traj_write is None:
            traj_write = n_itr // 100
        if restart_write is None:
            restart_write = n_itr // 100
        if pdb_wreite is None:
            pdb_wreite = n_itr // 100
        if checkpoint_write is None:
            checkpoint_write = n_itr // 10
        if transition_write is None:
            transition_write = n_itr // 10

        self.system_parameters = {
            "n_itr": n_itr,
            "time_step": time_step,
            "time_write": time_write,
            "traj_write": traj_write,
            "restart_write": restart_write,
            "pdb_wreite": pdb_wreite,
            "checkpoint_write": checkpoint_write,
            "transition_write": transition_write,
            "cluster_overlap_check": cluster_overlap_check,
            "overlap_sep_limit": overlap_sep_limit,
            "scale_max_displace": scale_max_displace,
        }

    def create_molecule_type(
        self,
        name: str,
        is_lipid: bool,
        is_implicit_lipid: bool,
        check_overlap: bool,
        count_transition: bool,
        transition_matrix_size: int,
        inside_compartment: str,
        outside_compartment: str,
        diffusion: np.array,
        rotation_diffusion: np.array,
        center_of_mass: np.array = np.array([0, 0, 0]),
        interface_names: list = [],
        interface_coords: list = [],
        bonds: list = [],
        states: list = [],
        mass: float = 1.0,
    ) -> "MoleculeType":
        """Create and register a MoleculeType object.

        Args:
            name (str): Name of the molecule type.
            is_lipid (bool): Whether the molecule type is a lipid.
            is_implicit_lipid (bool): Whether the lipid is implicit.
            check_overlap (bool): Whether to check overlap.
            count_transition (bool): Whether to count transitions between different assembly size.
            transition_matrix_size (int): Size of the transition matrix, which is the max possible assembly size.
            inside_compartment (bool): If this molecule type is inside the compartment.
            outside_compartment (bool): If this molecule type is outside the compartment.
            diffusion (np.array): The molecule’s translational diffusion constants in the x, y, and z directions, np.array([dx, dy, dz]). unit: um^2/s.
            rotation_diffusion (np.array): The molecule’s rotational diffusion constants in the alpha, theta, and phi directions, np.array([d1, d2, d3]). unit: rad^2/s.
            center_of_mass (np.array): Center of mass coordinates, default = np.array([0, 0, 0]). unit: nm.
            interface_names (list[str]): List of interface names.
            interface_coords (list[np.array]): List of interface coordinates. unit: nm.
            bonds (list[str]): List of bonds, default = interface_name, means that bond between the COM and interfaces.
            states (list[str]): List of states, ['interfaceName~P~U', ...]. means that the interfaceName has two states, P and U.
            mass (float): Mass of the molecule type, default = 1.

        Returns:
            MoleculeType: A new instance of MoleculeType.
        """
        molecule_type = MoleculeType(
            name, is_lipid, is_implicit_lipid, check_overlap, count_transition,
            transition_matrix_size, inside_compartment, outside_compartment,
            diffusion, rotation_diffusion, center_of_mass, interface_names,
            interface_coords, bonds, states, mass
        )
        self.molecule_types.append(molecule_type)
        return molecule_type

    def create_reaction(
        self,
        reactant1: str,
        interface1: str,
        reactant1_com: np.array,
        interface1_coord: np.array,
        reactant1_other_interfaces: list,
        reactant1_normal_point: np.array,
        reactant2: str,
        interface2: str,
        reactant2_com: np.array,
        interface2_coord: np.array,
        reactant2_other_interfaces: list,
        reactant2_normal_point: np.array,
        ka: float = None,
        kb: float = None,
        kon: float = 1,
        koff: float = 0.1,
        length_3d_2d: float = None,
        bind_radius_same_complex: float = 1.1,
        loop_coop_factor: float = 1.0,
        observe_label: str = None,
        reaction_label: str = None,
        coupled_reaction_label: str = None,
        kcat: float = None,
        exclude_volume_bound: bool = False,
    ) -> "Reaction":
        """Create and register a Reaction object.

        Args:
            reactant1 (str): Name of the first reactant.
            interface1 (str): Name of the first interface.
            reactant1_com (np.array): Center of mass of the first reactant. Global coordinates. unit: nm.
            interface1_coord (np.array): Coordinates of the first interface. Global coordinates. unit: nm.
            reactant1_other_interfaces (list): Other interfaces of the first reactant.
            reactant1_normal_point (np.array): Normal point of the first reactant. Global coordinates. unit: nm.
            reactant2 (str): Name of the second reactant.
            interface2 (str): Name of the second interface.
            reactant2_com (np.array): Center of mass of the second reactant. Global coordinates. unit: nm.
            interface2_coord (np.array): Coordinates of the second interface. Global coordinates. unit: nm.
            reactant2_other_interfaces (list): Other interfaces of the second reactant.
            reactant2_normal_point (np.array): Normal point of the second reactant. Global coordinates. unit: nm.
            ka (float): Association rate constant. default = None. unit: nm^3/(us).
            kb (float): Dissociation rate constant. default = None. unit: 1/s.
            kon (float): On rate constant. default = 1. unit: 1/(uM*s).
            koff (float): Off rate constant. default = 0.1. unit: 1/s.
            length_3d_2d (float): 3D to 2D length conversion factor. default = None. unit: nm.
            bind_radius_same_complex (float): Binding radius for the same complex. default = 1.1. unit: unitless.
            loop_coop_factor (float): Loop cooperativity factor. default = 1.0. unit: unitless.
            observe_label (str): Observation label. default = None.
            reaction_label (str): Reaction label. default = None.
            coupled_reaction_label (str): Label for coupled reactions. default = None.
            kcat (float): Catalytic rate constant. default = None. unit: 1/s.
            exclude_volume_bound (bool): Whether volume exclusion is applied. default = False.

        Returns:
            Reaction: A new instance of Reaction.
        """
        reaction = Reaction(
            reactant1, interface1, reactant1_com, interface1_coord,
            reactant1_other_interfaces, reactant1_normal_point, reactant2, interface2, reactant2_com,
            interface2_coord, reactant2_other_interfaces, reactant2_normal_point, ka, kb, kon, koff,
            length_3d_2d, bind_radius_same_complex, loop_coop_factor,
            observe_label, reaction_label, coupled_reaction_label, kcat,
            exclude_volume_bound
        )
        self.reactions.append(reaction)
        return reaction
    
    def visualize_molecule_types(self):
        """Visualize molecule types."""
        pass

    def visualize_binding_orientations(self):
        """Visualize binding orientations."""
        pass

    def write_mol_file(self, molecule_type: "MoleculeType"):
        """Write a molecule type to a mol file.

        Args:
            molecule_type (MoleculeType): Molecule type to write.
        """
        pass

    def write_inp_file(self):
        """Write an input file."""
        pass

    def write_nerdss_input_files(self):
        """Write NERDSS input file and mol files."""
        pass


class MoleculeType:
    """Represents a molecule type in NERDSS."""

    def __init__(self, *args):
        """Initialize a MoleculeType object.

        Args:
            *args: All parameters as described in `Model.create_molecule_type`.
        """
        (
            self.name, self.is_lipid, self.is_implicit_lipid, self.check_overlap,
            self.count_transition, self.transition_matrix_size,
            self.inside_compartment, self.outside_compartment, self.diffusion,
            self.rotation_diffusion, self.center_of_mass, self.interface_names,
            self.interface_coords, self.bonds, self.states, self.mass
        ) = args


class Reaction:
    """Represents a reaction in NERDSS."""

    def __init__(self, *args):
        """Initialize a Reaction object.

        Args:
            *args: All parameters as described in `Model.create_reaction`.
        """
        (
            self.reactant1, self.interface1, self.reactant1_com,
            self.interface1_coord, self.reactant1_other_interfaces,
            self.reactant1_normal_point,
            self.reactant2, self.interface2, self.reactant2_com,
            self.interface2_coord, self.reactant2_other_interfaces,
            self.reactant2_normal_point,
            self.ka, self.kb, self.kon, self.koff, self.length_3d_2d,
            self.bind_radius_same_complex, self.loop_coop_factor,
            self.observe_label, self.reaction_label,
            self.coupled_reaction_label, self.kcat, self.exclude_volume_bound
        ) = args

class Coords:
    """
    Holds the x, y, z coordinates of a 3D point. Includes basic vector arithmetic
    and distance calculation.

    Attributes:
        x (float): The x-coordinate.
        y (float): The y-coordinate.
        z (float): The z-coordinate.
    """
    def __init__(self, x: float, y: float, z: float):
        """
        Initializes a Coords instance.

        Args:
            x (float): x-coordinate.
            y (float): y-coordinate.
            z (float): z-coordinate.
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def distance(self, other) -> float:
        """
        Calculates the Euclidean distance between two points.

        Args:
            other (Coords): The other point to calculate the distance to.

        Returns:
            float: The Euclidean distance between the two points.
        """
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5

    def __sub__(self, other):
        """
        Implements subtraction for Coords objects.

        Args:
            other (Coords): The other coordinate to subtract.

        Returns:
            Coords: The resulting coordinate.
        """
        return Coords(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        """
        Implements addition for Coords objects.

        Args:
            other (Coords): The other coordinate to add.

        Returns:
            Coords: The resulting coordinate.
        """
        return Coords(self.x + other.x, self.y + other.y, self.z + other.z)
