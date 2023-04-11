from .dode_face_write import dode_face_write


def dode_face(radius: float, sigma: float):
    """
    Generates a dodecahedron face using the given radius and sigma values,
    writes it to a file using `dode_face_write` function, and prints a
    completion message.

    Args:
        radius (float): The radius of the dodecahedron.
        sigma (float): The sigma value to use for generating the dodecahedron.

    Returns:
        int: Always returns 0.

    Raises:
        None.

    Example:
        >>> dode_face(1.0, 0.5)
        File writing complete!
        0

    Note:
        The `dode_face_write` function is imported from `.dode_face_write` module,
        which is assumed to be in the same package as the current module.
    """
    
    dode_face_write(radius, sigma)
    print('File writing complete!')
    return 0


