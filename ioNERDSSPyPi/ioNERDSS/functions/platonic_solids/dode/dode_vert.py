from .dode_vert_write import dode_vert_write


def dode_vert(radius: float, sigma: float):
    """
    Generates and writes vertex coordinates for a dodecahedron to a file.

    Args:
        radius (float): Radius of the dodecahedron.
        sigma (float): Sigma value for generating vertex coordinates.

    Returns:
        int: 0 upon successful completion.

    Raises:
        FileNotFoundError: If the file to write vertex coordinates cannot be found.
        TypeError: If `radius` or `sigma` is not a float.

    Example:
        >>> dode_vert(1.0, 0.5)
        File writing complete!
        0
    """
    
    dode_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


