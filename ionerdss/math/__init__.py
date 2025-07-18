"""
ionerdss.math - Mathematical utilities and geometric functions.

This module provides mathematical utilities for molecular geometry,
coordinate transformations, and various computational operations.

Main classes and functions:
    Coords: 3D coordinate representation and operations
    Various angle calculation and rotation utilities
    Inertia tensor calculations
"""

from .coords import Coords
from .angles import *
from .rotations import *
from .inertia_tensors import *

__all__ = ['Coords']

# Import submodules and extend __all__ with their exports
from . import angles, rotations, inertia_tensors

__all__.extend(angles.__all__)
__all__.extend(rotations.__all__)
__all__.extend(inertia_tensors.__all__)