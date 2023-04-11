from .cube_face_write import cube_face_write


def cube_face(radius: float, sigma: float):
    """Generates a cube face file for visualization of a molecular system.

    This function generates a cube face file using the provided radius and sigma values, which can be used for
    visualization of a molecular system in a molecular visualization software. The cube face file is written using the
    `cube_face_write` function from the `.cube_face_write` module.

    Args:
        radius: A float specifying the radius of the cube face.
        sigma: A float specifying the sigma value for the cube face.

    Returns:
        An integer value of 0 indicating the completion of file writing.

    Raises:
        None.

    Example:
        >>> cube_face(3.5, 0.1)
        File writing complete!
        0
    """
    
    cube_face_write(radius, sigma)
    print('File writing complete!')
    return 0


