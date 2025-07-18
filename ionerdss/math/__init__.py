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

# Add all exports from submodules
import inspect
from . import angles, rotations, inertia_tensors

for module in [angles, rotations, inertia_tensors]:
    if hasattr(module, '__all__'):
        __all__.extend(module.__all__)
    else:
        # If no __all__ defined, export non-private functions
        __all__.extend([name for name, obj in inspect.getmembers(module)
                       if not name.startswith('_') and callable(obj)])