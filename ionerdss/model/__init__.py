"""
ionerdss.model - Molecular modeling and structure building tools.

This module provides tools for building and manipulating molecular models,
including PDB processing, complex assembly, and geometric structure generation.

Main classes:
    Model: Container for molecular systems and reactions
    MoleculeType: Definition of molecule types and their properties
    MoleculeInterface: Binding sites and interaction interfaces
    ReactionType: Reaction definitions and parameters
    PDBModel: PDB file processing and model extraction
    DesignModel: Systematic model design tools
"""

from .components import Model, MoleculeType, MoleculeInterface, Reaction
from .pdb_model import PDBModel
from .design_model import DesignModel
from .complex import generate_ode_model_from_pdb

__all__ = [
    'Model', 'MoleculeType', 'MoleculeInterface', 'Reaction',
    'PDBModel', 'DesignModel', 'generate_ode_model_from_pdb'
]