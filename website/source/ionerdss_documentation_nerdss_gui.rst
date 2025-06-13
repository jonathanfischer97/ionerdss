Integrated GUI for NERDSS simulation and analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import ionerdss as ion
    ion.nerdss()

This will open the NERDSS GUI, which allows you to prepare NERDSS inputs from PDB structure, run NERDSS simulations and analyze the results.

Setting Up Models for NERDSS Simulation Based on a PDB Structure File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each chain is mapped to a single molecule type. A molecule type consists of a Center of Mass (COM) and binding sites. The COM is the average position of all atoms in the chain. A binding site is the average position of all atoms in the contact area, which is determined by considering all pairs of amino acids within a specific cutoff distance.

.. important::
    To treat homo chains as same NERDSS molecule, use the `this jupyter notebook <pdb_to_nerdss_tutorial.html>`_ to prepare the NERDSS inputs.

.. figure:: ./fig/ionerdss_nerdss_gui_pdb.png
    :alt: PDB that we use in this tutorial
    :align: center
    :width: 50%

    PDB structure that we use in this tutorial.

Preparing and Selecting the PDB File in the User Interface
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: ./fig/ionerdss_nerdss_gui_parse.png
    :alt: Parse the PDB
    :align: center
    :width: 50%

    Parse the PDB structure with 3 clicks.

Generating NERDSS Inputs 
""""""""""""""""""""""""

.. figure:: ./fig/ionerdss_nerdss_gui_gen.png
    :alt: Generate NERDSS inputs
    :align: center
    :width: 50%

    Generate NERDSS inputs.

Modifying the Parameters as Needed
""""""""""""""""""""""""""""""""""

.. figure:: ./fig/ionerdss_nerdss_gui_modify.png
    :alt: Modify parameters
    :align: center
    :width: 50%

    Modify parameters as needed.

Clicking OK button will generate the NERDSS input files in the working directory
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: ./fig/ionerdss_nerdss_gui_save.png
    :alt: NERDSS input files saved
    :align: center
    :width: 100%

    NERDSS input files saved.

Running the Simulation
^^^^^^^^^^^^^^^^^^^^^^

Clicking the Install button will install NERDSS locally
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: ./fig/ionerdss_nerdss_gui_install.png
    :alt: Install NERDSS
    :align: center
    :width: 100%

    Install NERDSS locally.

Select nerdss executable and select the input files folder to run the simulation
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: ./fig/ionerdss_nerdss_gui_run.png
    :alt: Run the simulation
    :align: center
    :width: 50%

    Run the simulation.

Quickly Analyzing Simulation Outputs in the User Interface
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: ./fig/ionerdss_nerdss_gui_analyze.png
    :alt: Analyze the simulation outputs
    :align: center
    :width: 50%

    Analyze the simulation outputs.

.. figure:: ./fig/ionerdss_nerdss_gui_copynumber.png
    :alt: Graphing Copy Number of Species Over Time 
    :align: center
    :width: 100%

    Graphing Copy Number of Species Over Time.

.. figure:: ./fig/ionerdss_nerdss_gui_complex.png
    :alt: Graphing Complex Number Over Time
    :align: center
    :width: 100%

    Graphing Complex Number Over Time.