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