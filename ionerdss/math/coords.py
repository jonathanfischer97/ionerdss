"""
coords.py

Defines the `Coords` class, a lightweight 3D point representation with support for
basic vector operations and distance calculations.

This class is primarily used in NERDSS model construction to specify spatial positions
(e.g., interface coordinates on molecules) in simulations. It includes basic vector
arithmetic and helper methods for geometric reasoning.

Features:
- Vector addition and subtraction
- Euclidean distance calculation
- Human-readable string representation

Example:
    a = Coords(1.0, 2.0, 3.0)
    b = Coords(4.0, 6.0, 8.0)
    d = a.distance(b)
    c = a + b
"""

import math
from typing import Union, Iterable

Number = Union[int, float]

class Coords:
    """
    Represents a 3D point with x, y, z coordinates. Supports basic vector arithmetic
    and geometric operations.

    Attributes:
        x (float): x-coordinate.
        y (float): y-coordinate.
        z (float): z-coordinate.
    """

    def __init__(self, x: Number, y: Number, z: Number):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Coords") -> "Coords":
        return Coords(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def __repr__(self) -> str:
        return f"Coords(x={self.x:.3f}, y={self.y:.3f}, z={self.z:.3f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coords):
            return False
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z, other.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def distance_squared(self, other: "Coords") -> float:
        """
        Returns the squared Euclidean distance between self and another 
        point. It is used to avoid square root which is time consuming.
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return dx * dx + dy * dy + dz * dz

    
    def distance(self, other: "Coords") -> float:
        """Returns Euclidean distance between self and another point."""
        return math.dist(tuple(self), tuple(other))  # Python 3.8+

    def as_tuple(self):
        return (self.x, self.y, self.z)