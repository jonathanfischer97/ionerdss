"""
Module for generating ODE models from PDB structure complexes.

This module defines classes and functions to convert a coarse-grained PDB structure
into an ODE model that captures the assembly process of molecular complexes.
"""

from collections import defaultdict, deque
import itertools

class Complex:
    """
    Represents a molecular complex in an ODE (Ordinary Differential Equation) model.
    
    A complex can be a single molecule or multiple molecules bound together. This class
    tracks the structure of the complex in terms of molecule interactions.

    Attributes:
        structure_information_map (Dict[str, List[Tuple[Optional[str], Any]]]): 
            Maps molecule names to lists of (partner molecule name, reaction) tuples.
            If a molecule has no partner (single-molecule complex), partner is None.
    """
    def __init__(self):
        self.structure_information_map = {}

    def add_interaction(self, molecule, partner_molecule, reaction):
        """
        Adds an interaction to the structure information map.

        Args:
            molecule (CoarseGrainedMolecule): The molecule object.
            partner_molecule (CoarseGrainedMolecule): The partner molecule.
            reaction (Reaction): The reaction associated with the partner molecule.
        """
        if molecule not in self.structure_information_map:
            self.structure_information_map[molecule] = []
        self.structure_information_map[molecule].append((partner_molecule, reaction))

    def get_interactions(self, molecule):
        """
        Retrieves interactions for a given molecule.

        Args:
            molecule (str): The molecule name.

        Returns:
            list: A list of tuples containing partner molecule names and their associated reactions.
        """
        return self.structure_information_map.get(molecule, [])

    def get_keys(self):
        """
        Retrieves all keys (molecule names) in the structure information map.

        Returns:
            list: A list of molecule names.
        """
        return list(self.structure_information_map.keys())
    
    def size(self):
        """
        Returns the number of molecules in the complex.
        
        Returns:
            int: The number of molecules.
        """
        return len(self.structure_information_map)
    
    def all_partners(self, molecule):
        """
        Gets all partner molecules for a given molecule.
        
        Args:
            molecule: The molecule name.
            
        Returns:
            List[str]: List of partner molecule names.
        """
        interactions = self.get_interactions(molecule)
        return [partner for partner, _ in interactions if partner is not None]
    
    def generate_signature(self):
        """
        Returns a unique signature representing the complex structure.
        
        For single molecule complexes: frozenset with the molecule name
        For multi-molecule complexes: frozenset of sorted molecule name pairs
        
        Returns:
            FrozenSet: A unique signature for this complex.
        """
        if not self.structure_information_map:
            return frozenset()

        keys = list(self.structure_information_map.keys())

        # Single molecule with no partners
        if len(keys) == 1 and (not self.structure_information_map[keys[0]] or 
                             all(partner is None for partner, _ in self.structure_information_map[keys[0]])):
            return frozenset([keys[0].name])

        # Multi-molecule complex: collect undirected molecule pairs as signature
        edges = set()
        for mol, partners in self.structure_information_map.items():
            for partner, _ in partners:
                if partner:  # Skip None
                    edge = tuple(sorted((mol.name, partner.name)))
                    edges.add(edge)

        return frozenset(edges)
    
    def is_subset_of(self, other_complex):
        """
        Checks if this complex is a subset of another complex.
        
        Args:
            other_complex (Complex): The other complex to compare with.
            
        Returns:
            bool: True if this complex is a subset of other_complex, False otherwise.
        """
        if not isinstance(other_complex, Complex):
            return False
            
        this_sig = self.generate_signature()
        other_sig = other_complex.generate_signature()
        
        # Special case for single molecule complexes
        if len(this_sig) == 1 and list(this_sig)[0] in other_complex.get_keys():
            return True
            
        # Check if all edges in this complex are in the other complex
        return this_sig.issubset(other_sig)
    
    def get_topology_type(self):
        """
        Determine if the complex has a linear, cyclic, or branched topology.
        
        Returns:
            str: The topology type ("linear", "cyclic", "branched", or "single").
        """
        if self.size() == 1:
            return "single"
            
        edges = self.generate_signature()
        if not edges:
            return "single"
            
        # Build adjacency structure from edges
        adjacency = defaultdict(list)
        for a, b in edges:
            adjacency[a].append(b)
            adjacency[b].append(a)
        
        # Count connections per node
        connection_counts = {node: len(connections) for node, connections in adjacency.items()}
        
        # Linear: exactly 2 nodes have 1 connection, the rest have 2
        # Cyclic: all nodes have exactly 2 connections
        # Branched: at least one node has more than 2 connections
        
        if all(count == 2 for count in connection_counts.values()):
            return "cyclic"
        elif list(connection_counts.values()).count(1) == 2 and all(count == 1 or count == 2 for count in connection_counts.values()):
            return "linear"
        else:
            return "branched"

    def to_reaction_string(self):
        """
        Converts the complex to a reaction string representation.
        
        Returns:
            str: A string representation of the complex suitable for reactions.
        """
        molecules = self.get_keys()

        # convert molecules to molecule names
        molecules = [molecule.name for molecule in molecules]
        
        if len(molecules) == 1:
            return molecules[0]
        
        # Sort molecules for consistent base representation
        molecules = sorted(molecules)
        base_repr = ".".join(molecules)
        
        # Get general topology type
        topology = self.get_topology_type()
        
        # Use a hash of the edge set to uniquely identify the topology
        signature = self.generate_signature()
        sig_hash = hash(signature) % 10000  # Keep it reasonably short
        
        return f"{base_repr}[{topology}-{sig_hash:04d}]"

    def __repr__(self):
        molecules = self.get_keys()
        
        if len(molecules) == 1:
            return f"Complex({molecules[0].my_template.name})"
        
        # Include binding topology in the representation
        topology = self.get_topology_type()

        sorted_molecules = sorted(molecules, key=lambda m: m.my_template.name)
        joined_names = '-'.join(m.my_template.name for m in sorted_molecules)

        reactions = []
        for self_key in self.get_keys():
            for partner, reaction in self.get_interactions(self_key):
                if partner is not None:
                    reactions.append(reaction.my_template.expression)
        reactions = sorted(reactions)
        # there are two same reactions for each edge
        reactions = reactions[::2]
        joined_reactions = ', '.join(reactions)
        
        return f"Complex({joined_names}, {topology}, {joined_reactions})"

    def __eq__(self, other):
        if not isinstance(other, Complex):
            return False

        if self.size() != other.size():
            return False
        
        # the key.my_template.name should have a one-on-one mapping between the two complexes
        # get the keys of self
        self_keys = self.get_keys()
        # convert the keys to a list of their template names
        self_template_names = [key.my_template.name for key in self_keys]
        # get the keys of other
        other_keys = other.get_keys()
        # convert the keys to a list of their template names
        other_template_names = [key.my_template.name for key in other_keys]
        # sort the two lists and compare
        if sorted(self_template_names) != sorted(other_template_names):
            return False
        
        if self.size() == 1:
            return True
        
        # the edges should have a one-on-one mapping between the two complexes
        self_edges = []
        for key in self_keys:
            self_edges += [sorted((key.my_template.name, partner.my_template.name, reaction.my_template.expression)) for partner, reaction in self.get_interactions(key)]
        self_edges = sorted(self_edges)
        other_edges = []
        for key in other_keys:
            other_edges += [sorted((key.my_template.name, partner.my_template.name, reaction.my_template.expression)) for partner, reaction in other.get_interactions(key)]
        other_edges = sorted(other_edges)
        if self_edges != other_edges:
            return False
        
        return True
    
    def __hash__(self):
        return hash(self.generate_signature())
    
    
class ComplexReaction:
    """
    Represents a reaction between molecular complexes.
    
    This class models association, dissociation, or other transformations
    involving molecular complexes in an ODE system.
    
    Attributes:
        reactants (List[Complex]): List of reactant complexes.
        products (List[Complex]): List of product complexes.
        reaction_type (str): Type of reaction (e.g., "association", "dissociation").
        reaction_string (str): String representation of the reaction.
    """
    def __init__(self, reactants=None, products=None, reaction_type=None):
        """
        Initialize a complex reaction.
        
        Args:
            reactants (List[Complex], optional): List of reactant complexes.
            products (List[Complex], optional): List of product complexes.
            reaction_type (str, optional): Type of reaction.
        """
        self.reactants = reactants or []
        self.products = products or []
        self.reaction_type = reaction_type
        self._generate_reaction_string()
    
    def _generate_reaction_string(self):
        """Generate the reaction string representation."""
        reactant_strings = [r.to_reaction_string() for r in self.reactants]
        product_strings = [p.to_reaction_string() for p in self.products]
        
        reactant_part = " + ".join(reactant_strings)
        product_part = " + ".join(product_strings)
        
        self.reaction_string = f"{reactant_part} -> {product_part}"
    
    def is_association(self):
        """
        Check if this is an association reaction (A + B -> AB).
        
        Returns:
            bool: True if this is an association reaction.
        """
        return len(self.reactants) > 1 and len(self.products) == 1
    
    def is_dissociation(self):
        """
        Check if this is a dissociation reaction (AB -> A + B).
        
        Returns:
            bool: True if this is a dissociation reaction.
        """
        return len(self.reactants) == 1 and len(self.products) > 1
    
    def __repr__(self):
        return f"ComplexReaction({self.reaction_string})"
    
    def __eq__(self, other):
        if not isinstance(other, ComplexReaction):
            return False
        return self.reaction_string == other.reaction_string
    
    def __hash__(self):
        return hash(self.reaction_string)

class ComplexReactionSystem:
    """
    Represents a system of complex reactions for ODE modeling.

    This class tracks reactions between complexes and their associated rates
    for use in constructing ODEs that model complex assembly.
    
    Attributes:
        reactions (List[ComplexReaction]): List of reactions in the system.
        rates (Dict[ComplexReaction, float]): Map of reactions to their rates.
        complexes (List[Complex]): List of all complexes in the system.
    """
    def __init__(self):
        """Initialize an empty reaction system."""
        self.reactions = []
        self.rates = {}
        self.complexes = []
        self.complex_map = {}  # Maps complex signatures to Complex objects

    def add_complex(self, complex_obj):
        """
        Add a complex to the system if it's not already present.
        
        Args:
            complex_obj (Complex): The complex to add.
            
        Returns:
            Complex: The added complex or the existing equivalent complex.
        """
        signature = complex_obj.generate_signature()
        
        if signature in self.complex_map:
            return self.complex_map[signature]
            
        self.complexes.append(complex_obj)
        self.complex_map[signature] = complex_obj
        return complex_obj

    def add_reaction(self, reaction, rate=1.0):
        """
        Add a reaction and its rate to the system.

        Args:
            reaction (ComplexReaction): The reaction to add.
            rate (float, optional): The rate of the reaction. Defaults to 1.0.
            
        Returns:
            ComplexReaction: The added reaction.
        """
        if reaction not in self.reactions:
            self.reactions.append(reaction)
        self.rates[reaction] = rate
        return reaction

    def get_rate(self, reaction):
        """
        Get the rate of a reaction.

        Args:
            reaction (ComplexReaction): The reaction.

        Returns:
            float: The rate of the reaction, or None if not found.
        """
        return self.rates.get(reaction)
    
    def get_all_complexes_of_size(self, size):
        """
        Get all complexes of a specific size.
        
        Args:
            size (int): The number of molecules in the complex.
            
        Returns:
            List[Complex]: List of complexes with the specified size.
        """
        return [c for c in self.complexes if c.size() == size]
    
    def generate_ode_equations(self):
        """
        Generate ODE equations for the reaction system.
        
        Returns:
            str: A string representing the system of ODEs.
        """
        # This would generate actual ODE equations based on the reactions and rates
        # For now, just return a placeholder
        equations = []
        
        # Track term contributions for each complex
        complex_terms = {complex_obj: [] for complex_obj in self.complexes}
        
        # For each reaction, add appropriate terms to the ODEs
        for reaction in self.reactions:
            rate = self.rates[reaction]
            rate_term = f"{rate}"
            
            # Mass action kinetics: rate * product of reactant concentrations
            reactant_term = " * ".join(r.to_reaction_string() for r in reaction.reactants)
            
            for reactant in reaction.reactants:
                # Negative term: reactant is consumed
                complex_terms[reactant].append(f"-{rate_term} * {reactant_term}")
                
            for product in reaction.products:
                # Positive term: product is produced
                complex_terms[product].append(f"+{rate_term} * {reactant_term}")
        
        # Construct the ODEs
        for complex_obj, terms in complex_terms.items():
            if terms:
                terms_str = " ".join(terms)
                equation = f"d[{complex_obj.to_reaction_string()}]/dt = {terms_str}"
                equations.append(equation)
            else:
                # No terms - either a basic species or isolated
                equation = f"d[{complex_obj.to_reaction_string()}]/dt = 0"
                equations.append(equation)
        
        return "\n".join(equations)

    def __repr__(self):
        return f"ComplexReactionSystem with {len(self.complexes)} complexes and {len(self.reactions)} reactions"
    
def parse_complexes_from_pdb_model(pdb_model, max_complex_size=None):
    """
    Parse all connected complexes from a PDB model structure.
    
    This function identifies all possible molecular complexes that can form based on
    the binding interfaces in the PDB structure.
    
    Args:
        pdb_model: The PDBModel object containing molecules and reactions.
        max_complex_size (int, optional): Maximum number of molecules in a complex.
            If None, no limit is applied. Defaults to None.
            
    Returns:
        List[Complex]: List of all possible complexes.
    """
    # Helper functions for checking connectivity
    def build_connectivity_graph(molecules, reaction_list):
        """Build a graph representing molecule connectivity."""
        graph = defaultdict(set)
        for reaction in reaction_list:
            if not reaction.reactants or len(reaction.reactants) != 2:
                continue
                
            m1, m2 = reaction.reactants[0][0], reaction.reactants[1][0]
            graph[m1.name].add((m2.name, reaction))
            graph[m2.name].add((m1.name, reaction))
        return graph
    
    def are_molecules_connected(molecule_subset, connectivity_graph):
        """Check if the molecules in subset form a connected component."""
        if not molecule_subset:
            return False
            
        # Convert to name-based set for easier lookup
        molecule_names = {m.name for m in molecule_subset}
        if len(molecule_names) == 1:
            return True  # Single molecule is trivially connected
            
        # Do a BFS to check connectivity
        visited = set()
        queue = deque([molecule_subset[0].name])
        
        while queue:
            current = queue.popleft()
            visited.add(current)
            
            for neighbor, _ in connectivity_graph[current]:
                if neighbor not in visited and neighbor in molecule_names:
                    queue.append(neighbor)
        
        return len(visited) == len(molecule_names)
    
    def find_valid_binding_edges(molecule_subset, connectivity_graph):
        """Find all valid binding edges between molecules in the subset."""
        valid_edges = []
        checked_pairs = set()
        
        for molecule in molecule_subset:
            for partner, reaction in connectivity_graph[molecule.name]:
                # Check if this partner is in our subset
                partner_molecule = next((m for m in molecule_subset if m.name == partner), None)
                if not partner_molecule:
                    continue
                    
                # Avoid duplicate edges (A-B vs B-A)
                pair = tuple(sorted([molecule.name, partner]))
                if pair in checked_pairs:
                    continue
                    
                checked_pairs.add(pair)
                valid_edges.append((molecule, partner_molecule, reaction))
                
        return valid_edges
    
    def is_edge_subset_connected(molecule_subset, edge_subset):
        """Check if the selected edges form a connected subgraph."""
        if not edge_subset:
            return False
            
        # Build a graph from just these edges
        graph = defaultdict(set)
        for m1, m2, _ in edge_subset:
            graph[m1.name].add(m2.name)
            graph[m2.name].add(m1.name)
        
        # Check connectivity with BFS
        visited = set()
        queue = deque([molecule_subset[0].name])
        molecule_names = {m.name for m in molecule_subset}
        
        while queue:
            current = queue.popleft()
            visited.add(current)
            
            for neighbor in graph[current]:
                if neighbor not in visited and neighbor in molecule_names:
                    queue.append(neighbor)
        
        return len(visited) == len(molecule_names)
    
    # Main algorithm implementation
    all_molecules = pdb_model.molecule_list
    connectivity_graph = build_connectivity_graph(all_molecules, pdb_model.reaction_list)
    
    complex_list = []
    
    # Limit complex size if specified
    max_size = max_complex_size or len(all_molecules)
    max_size = min(max_size, len(all_molecules))
    
    # Handle single-molecule complexes first
    for molecule in all_molecules:
        complex_obj = Complex()
        complex_obj.add_interaction(molecule, None, None)
        
        if complex_obj not in complex_list:
            complex_list.append(complex_obj)
    
    # Handle multi-molecule complexes (sizes 2 to max_size)
    for size in range(2, max_size + 1):
        # Generate all size-molecule subsets
        for molecule_subset in itertools.combinations(all_molecules, size):
            molecule_subset = list(molecule_subset)
            
            # Skip disconnected subsets
            if not are_molecules_connected(molecule_subset, connectivity_graph):
                continue
            
            # Find all valid binding edges
            valid_edges = find_valid_binding_edges(molecule_subset, connectivity_graph)
            
            # Generate all possible connected edge subsets
            # Start with the minimum spanning tree size (n-1 edges)
            min_edges = len(molecule_subset) - 1
            
            # Try increasing numbers of edges up to all valid edges
            for edge_count in range(min_edges, len(valid_edges) + 1):
                for edge_subset in itertools.combinations(valid_edges, edge_count):
                    edge_subset = list(edge_subset)
                    
                    # Skip edge subsets that don't connect all molecules
                    if not is_edge_subset_connected(molecule_subset, edge_subset):
                        continue
                    
                    # Create a complex with this configuration
                    complex_obj = Complex()
                    
                    # Add bidirectional interactions for each edge
                    for m1, m2, reaction in edge_subset:
                        complex_obj.add_interaction(m1, m2, reaction)
                        complex_obj.add_interaction(m2, m1, reaction)
                    
                    # Add the complex to the list if not already present
                    if complex_obj not in complex_list:
                        complex_list.append(complex_obj)
    
    return complex_list


def build_ode_model_from_complexes(complex_list, pdb_model=None, default_association_rate=1.0, default_dissociation_rate=0.1):
    """
    Build an ODE model from a list of complexes.
    
    This function generates association and dissociation reactions between complexes
    to model the assembly process.
    
    Args:
        complex_list (List[Complex]): List of all possible complexes.
        pdb_model (optional): PDB model with reaction information.
        default_association_rate (float, optional): Default rate for association reactions.
        default_dissociation_rate (float, optional): Default rate for dissociation reactions.
        
    Returns:
        ComplexReactionSystem: The populated reaction system.
    """
    # Initialize reaction system and add all complexes
    reaction_system = ComplexReactionSystem()
    for complex_obj in complex_list:
        reaction_system.add_complex(complex_obj)
    
    # Generate all possible association reactions
    for i, complex1 in enumerate(complex_list):
        if complex1.size() == 1:  # Basic molecule
            # Find all complexes that can form from this basic molecule
            for complex2 in complex_list:
                if complex2.size() > 1 and complex1.is_subset_of(complex2):
                    # Find the complementary part
                    complementary_keys = set(complex2.get_keys()) - set(complex1.get_keys())
                    if not complementary_keys:
                        continue
                        
                    # Find a complex matching the complementary part
                    for complex3 in complex_list:
                        if set(complex3.get_keys()) == complementary_keys:
                            # A + B -> AB association reaction
                            association = ComplexReaction(
                                reactants=[complex1, complex3],
                                products=[complex2],
                                reaction_type="association"
                            )
                            reaction_system.add_reaction(association, default_association_rate)
                            
                            # AB -> A + B dissociation reaction
                            dissociation = ComplexReaction(
                                reactants=[complex2],
                                products=[complex1, complex3],
                                reaction_type="dissociation"
                            )
                            reaction_system.add_reaction(dissociation, default_dissociation_rate)
        
        # Larger complex association (e.g., A.B + C -> A.B.C)
        elif complex1.size() > 1:
            for complex2 in complex_list:
                # Skip if same complex or if complex2 is very large
                if complex1 == complex2 or complex2.size() > complex1.size():
                    continue
                    
                # Try to find a larger complex that contains both complex1 and complex2
                for complex3 in complex_list:
                    if (complex3.size() == complex1.size() + complex2.size() and
                        set(complex3.get_keys()) == set(complex1.get_keys()) | set(complex2.get_keys())):
                        
                        # Check if the merger is valid based on binding interactions
                        valid_merger = False
                        for m1 in complex1.get_keys():
                            for m2 in complex2.get_keys():
                                # Check if there's a binding interaction in the target complex
                                if m2 in complex3.all_partners(m1):
                                    valid_merger = True
                                    break
                            if valid_merger:
                                break
                                
                        if valid_merger:
                            # Create association reaction
                            association = ComplexReaction(
                                reactants=[complex1, complex2],
                                products=[complex3],
                                reaction_type="association"
                            )
                            reaction_system.add_reaction(association, default_association_rate)
                            
                            # Create dissociation reaction
                            dissociation = ComplexReaction(
                                reactants=[complex3],
                                products=[complex1, complex2],
                                reaction_type="dissociation"
                            )
                            reaction_system.add_reaction(dissociation, default_dissociation_rate)
    
    # If we have a PDB model, we could refine rates based on reaction properties
    if pdb_model:
        _refine_rates_from_pdb_model(reaction_system, pdb_model)
    
    return reaction_system


def _refine_rates_from_pdb_model(reaction_system, pdb_model):
    """
    Refine reaction rates based on PDB model information.
    
    Args:
        reaction_system (ComplexReactionSystem): The reaction system.
        pdb_model: The PDB model with reaction information.
    """
    # This would use binding energies or other factors from the PDB model
    # to refine the default reaction rates
    pass


def generate_ode_model_from_pdb(pdb_model, max_complex_size=None):
    """
    Generate a complete ODE model from a PDB structure.
    
    This is the main function that orchestrates the full process:
    1. Parse all possible complexes from the PDB structure
    2. Build an ODE reaction system
    3. Return the populated system
    
    Args:
        pdb_model: The PDBModel object.
        max_complex_size (int, optional): Maximum number of molecules in a complex.
        
    Returns:
        Tuple[List[Complex], ComplexReactionSystem]: The list of complexes and
        the reaction system.
    """
    # Parse all possible complexes
    all_complexes = parse_complexes_from_pdb_model(pdb_model, max_complex_size)
    
    # Build the reaction system
    reaction_system = build_ode_model_from_complexes(all_complexes, pdb_model)
    
    return all_complexes, reaction_system
