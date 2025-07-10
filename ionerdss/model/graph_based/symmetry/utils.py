"""
This file includes code adapted from the 'pointgroup' package,
originally authored by Abel Carreras (https://github.com/abelcarreras/pointgroup),
and is licensed under the MIT License:

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

def magic_formula(n):
    """
    Compute the value of the expression: sqrt(n * 2^(3 - n))

    This "magic formula" may be used in contexts where the geometric scaling or 
    normalization of an n-mer system is required, such as symmetry-based energy or 
    entropy factors in molecular assemblies.

    Parameters
    ----------
    n : int or float
        The input value (typically an integer ≥ 1), e.g., number of subunits or symmetry order.

    Returns
    -------
    float
        The computed value of sqrt(n * 2^(3 - n))

    Examples
    --------
    >>> magic_formula(2)
    2.0
    >>> magic_formula(3)
    1.732...
    """
    return np.sqrt(n * 2 ** (3 - n))

def normalized_radius_difference(reference_vec, targets, tol=1e-5):
    """
    Compute the relative radial distance differences (unitless),
    normalized by average radius between a reference vector and each target.

    Parameters
    ----------
    reference_vec : array_like of shape (3,)
        Reference 3D vector.
    targets : ndarray of shape (N, 3)
        Array of target 3D vectors.
    tol : float
        Minimum average radius to avoid divide-by-zero.

    Returns
    -------
    rel_differences : ndarray of shape (N,)
        Array of absolute radius differences normalized by average radius.
    """
    ref_norm = np.linalg.norm(reference_vec)
    target_norms = np.linalg.norm(targets, axis=1)

    avg_radii = np.clip((target_norms + ref_norm) / 2.0, tol, None)
    abs_diff = np.abs(target_norms - ref_norm)

    return abs_diff / avg_radii
