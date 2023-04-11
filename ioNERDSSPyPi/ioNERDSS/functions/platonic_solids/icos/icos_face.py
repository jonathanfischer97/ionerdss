from .icos_face_write import icos_face_write


def icos_face(radius: float, sigma: float):
    """
    Write an icosahedron face with given radius and sigma to a file.

    This function writes an icosahedron face with the given radius and sigma values
    to a file using the `icos_face_write()` function from the `icos_face_write` module.

    Args:
        radius (float): The radius of the icosahedron face.
        sigma (float): The sigma value for the icosahedron face.

    Returns:
        int: Always returns 0 to indicate successful completion.

    Raises:
        None

    Examples:
        >>> radius = 1.0
        >>> sigma = 0.5
        >>> icos_face(radius, sigma)
        File writing complete!
        0

    Notes:
        This function is dependent on the `icos_face_write()` function from the `icos_face_write` module,
        which should be imported properly before calling this function. The function writes the icosahedron
        face to a file and prints a message indicating that the file writing is complete.
    """
    icos_face_write(radius, sigma)
    print('File writing complete!')
    return 0


