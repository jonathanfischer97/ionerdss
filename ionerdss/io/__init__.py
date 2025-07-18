"""
ionerdss.io - Input/output and data conversion utilities.

This module provides functions for reading, writing, and converting
data between different formats used in NERDSS simulations.
"""

# Import simularium converter
from .simularium.simularium_converter import convert_simularium

__all__ = ['convert_simularium']