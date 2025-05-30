Gag self assembly model
~~~~~~~~~~~~~~~~~~~~~~~~

This section describes how to set up a model for Gag self-assembly.

Reshape Gag
^^^^^^^^^^^

reshape_gag(PathName)

**Description:** 
Constructs a model of the Gag monomer. Experimentally measured Gag lattice structures must be regularized to eliminate thermal fluctuations and other experimental errors. This function reshapes and regularizes these structures.

**Parameters:**

- **PathName** (string): The path of the .pdb file.

**Returns:**

- **finalPositionsVec** (list of shape 144 x 3): The coordinates of the center of mass (COM) and 5 interfaces for each of the 18 Gag monomers.

**Example:**

.. code-block:: python

    import ionerdss as ion
    finalPositionsVec = ion.reshape_gag('path/to/file.pdb')
