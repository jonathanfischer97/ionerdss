"""
angles.py

This module provides utility functions for analyzing geometric and rotational
symmetries of point-based structures (e.g., molecular assemblies) using inertia tensors
and vector algebra. These tools are particularly useful for identifying symmetry axes
and classifying point group symmetries in 3D configurations such as molecular complexes,
polyhedral assemblies, and coarse-grained models.

Note: This file includes code adapted from the 'pointgroup' package,
originally authored by Abel Carreras (https://github.com/abelcarreras/pointgroup),
and is licensed under the MIT License (which is attached to the end of this docstring)

Included Functions
------------------

1. get_inertia_tensor(coords, tol=1e-12)
    Computes the normalized moment of inertia tensor for a set of 3D points,
    assuming uniform mass. Returns a symmetric 3×3 tensor that characterizes
    how mass is distributed relative to the center of mass.

2. get_degeneracy(eigenvalues, tolerance=0.1)
    Estimates the degeneracy (repeatedness) of eigenvalues within a specified tolerance.
    Useful for inferring rotational symmetry based on isotropy of the inertia tensor.

3. get_non_degenerated(eigenvalues, tolerance=0.1)
    Identifies which eigenvalue in a set of three is non-degenerate, assuming
    two are nearly equal. Often used to detect symmetry axes.

4. get_perpendicular_vector(vector, normalize=True, tol=1e-8)
    Computes a vector orthogonal to a given input vector. Supports general n-dimensional input.
    For 3D vectors, uses the cross product; for nD, falls back to Gram-Schmidt projection.

Use Cases
---------
- Classifying molecular shapes and point group symmetries from 3D atomic coordinates
- Determining principal axes of rotation
- Automatically choosing reference frames based on geometry
- Computing orientation-aware quantities from molecular subunits

Dependencies
------------
- numpy

Examples
--------
>>> coords = np.array([[1,0,0], [-1,0,0], [0,1,0], [0,-1,0]])
>>> I = get_inertia_tensor(coords)
>>> eigvals, eigvecs = np.linalg.eigh(I)
>>> degeneracy = get_degeneracy(eigvals)
>>> main_axis_idx = get_non_degenerated(eigvals)
>>> perp = get_perpendicular_vector(eigvecs[:, main_axis_idx])




The MIT License (MIT)

Copyright (c) 2023 Efrem Bernuz and Abel Carreras

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import numpy as np

def absolute_error_to_angle(error, points, tol=1e-8):
    """
    Convert absolute coordinate errors to angular errors (in radians),
    assuming origin-centered radial vectors.

    Parameters
    ----------
    error : float
        Absolute positional error (e.g., in angstroms or nanometers).
    points : ndarray of shape (N, 3)
        Array of 3D coordinates representing points from origin.
    tol : float
        Minimum radius threshold to avoid divide-by-zero.

    Returns
    -------
    angle_errors : ndarray of shape (N,)
        Angular errors in radians for each point.
    """
    points = np.asarray(points)
    radii = np.linalg.norm(points, axis=1)
    clipped_radii = np.clip(radii, tol, None)
    return error / clipped_radii

def angles_between_vector_and_vectors(reference_vec, targets, tol=1e-5):
    """
    Compute angles (in radians) between a reference vector and each row in a matrix.

    Parameters
    ----------
    reference_vec : array_like of shape (3,)
        The reference 3D vector.
    targets : ndarray of shape (N, 3)
        Array of target 3D vectors to compute angles with respect to.
    tol : float
        Threshold below which vector norms are treated as zero.

    Returns
    -------
    angles : ndarray of shape (N,)
        Array of angles (in radians) between reference vector and each target vector.
    """
    targets = np.asarray(targets)
    ref_norm = np.linalg.norm(reference_vec)
    target_norms = np.linalg.norm(targets, axis=1)

    dot_products = np.dot(targets, reference_vec)

    angles = []
    for dot, target_norm in zip(dot_products, target_norms):
        denom = target_norm * ref_norm
        if denom < tol:
            angles.append(0.0)
        else:
            cos_theta = np.clip(dot / denom, -1.0, 1.0)
            angles.append(np.arccos(cos_theta))
    return np.array(angles)