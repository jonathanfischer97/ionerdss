from scipy.spatial.transform import Rotation as R
import numpy as np

def rotation_matrix(axis, angle, tol=1e-8):
    """
    Compute the 3D rotation matrix for a rotation around a given axis by a specified angle.
    A wrapper for scipy.spatial.transform.Rotation

    Parameters
    ----------
    axis : array-like of shape (3,)
        The axis of rotation. This vector will be normalized internally.
    angle : float
        The rotation angle in radians.
    tol : float, optional
        Tolerance for checking whether the axis is non-zero. Default is 1e-8.

    Returns
    -------
    ndarray of shape (3, 3)
        A 3×3 rotation matrix representing the rotation about the given axis.

    Raises
    ------
    ValueError
        If the provided axis has near-zero length.
    """
    axis = np.asarray(axis, dtype=float)
    norm = np.linalg.norm(axis)
    if norm < tol:
        raise ValueError("Axis must be a non-zero vector")

    axis = axis / norm
    return R.from_rotvec(angle * axis).as_matrix()

class Rotation:
    """
    Represents a proper Cn rotation (n-fold symmetry) about a specified axis.

    This class constructs a 3D rotation matrix for a rotation by 2π/n radians
    around the given axis. It is used to represent symmetry operations like
    those found in molecular point groups.

    Parameters
    ----------
    axis : array-like of shape (3,)
        The axis about which the rotation is performed. It will be normalized internally.
    order : int, optional
        The symmetry order (n). A rotation of 2π/n radians will be applied. Default is 1.

    Methods
    -------
    get_matrix() -> ndarray
        Returns the 3×3 proper rotation matrix.
    """
    def __init__(self, axis, order=1):
        self._axis = np.asarray(axis, dtype=float)
        self._order = order

    def get_matrix(self):
        """Return the proper rotation matrix (Cn) of 2π / n about the axis."""
        angle = 2 * np.pi / self._order
        return rotation_matrix(self._axis, angle)

class ImproperRotation:
    """
    Represents an improper Sn rotation: a Cn rotation followed by reflection.

    An improper rotation consists of:
    - A proper rotation of 2π/n radians around a specified axis
    - Followed by a reflection through the plane perpendicular to that axis

    This operation is used to represent symmetry elements like mirror-rotations
    in molecular and crystallographic point groups.

    Parameters
    ----------
    axis : array-like of shape (3,)
        The axis for both the rotation and the perpendicular reflection.
        This vector will be normalized internally.
    order : int, optional
        The symmetry order n (i.e., the "n" in Sn). Default is 1.

    Methods
    -------
    get_matrix() -> ndarray
        Returns the 3×3 matrix for the improper rotation operation.
    """
    def __init__(self, axis, order=1):
        self._axis = np.asarray(axis, dtype=float)
        self._order = order

    def get_matrix(self):
        """Return the improper rotation matrix (Cn followed by reflection)."""
        angle = 2 * np.pi / self._order
        rot = rotation_matrix(self._axis, angle)

        # Reflection across the plane perpendicular to axis: I - 2 uuᵀ
        u = self._axis / np.linalg.norm(self._axis)
        refl = np.eye(3) - 2 * np.outer(u, u)

        return rot @ refl.T  # rot ∘ reflect
