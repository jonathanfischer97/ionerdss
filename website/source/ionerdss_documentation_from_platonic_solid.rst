Platonic Solid Self-assembly Input File Writing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Platonic solid self-assembly includes 10 models, each requiring a separate function. The names of the functions are listed in the following table:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - **Platonic Solid**
     - **Center-of-Mass Position**
     - **Name of Function**
   * - Tetrahedron (4-face)
     - Each Face
     - ``tetr_face(radius, sigma)``
   * - Tetrahedron (4-face)
     - Each Vertex
     - ``tetr_vert(radius, sigma)``
   * - Cube (6-face)
     - Each Face
     - ``cube_face(radius, sigma)``
   * - Cube (6-face)
     - Each Vertex
     - ``cube_vert(radius, sigma)``
   * - Octahedron (8-face)
     - Each Face
     - ``octa_face(radius, sigma)``
   * - Octahedron (8-face)
     - Each Vertex
     - ``octa_vert(radius, sigma)``
   * - Dodecahedron (12-face)
     - Each Face
     - ``dode_face(radius, sigma)``
   * - Dodecahedron (12-face)
     - Each Vertex
     - ``dode_vert(radius, sigma)``
   * - Icosahedron (20-face)
     - Each Face
     - ``icos_face(radius, sigma)``
   * - Icosahedron (20-face)
     - Each Vertex
     - ``icos_vert(radius, sigma)``

Description:
    Generates NERDSS input files (.inp and .mol files) for Platonic solid self-assembly systems.

Parameters:
    - ``radius`` (float): The radius of the Platonic solid in nm, defined as the distance from the center of the Platonic solid to each vertex.
    - ``sigma`` (float): The distance of each interface when a reaction takes place in nm.

- Here is a Jupyter notebook that demonstrates how to set up a model for Platonic solid self-assembly:  

  `model_setup_for_platonic_solid <model_setup_for_platonic_solid.html>`_