Create NERDSS Input from PDB Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The jupyter notebook `pdb_to_nerdss_tutorial <pdb_to_nerdss_tutorial.html>`_ demonstrates how to convert a PDB file into a NERDSS input file, with the ability to regularize the homo chains in the PDB to consistent NERDSS molecule.

ionerdss also provides some other tools to treat the PDB files:

- PDB_UI()

    - **Description:** This function reads in the PDB file and creates a NERDSS input. This function will treate each chain in PDB as a different NERDSS molecule. Note that this cannot be run in a Jupyter Notebook, as it requires a command line to output text and get user input.
    
    - **Usage:** Open Python in the command line, import `ionerdss`, then call `PDB_UI()`.

    - **Tutorial:**
        1. Store a PDB file in the working directory.
        
        2. Call this function with an appropriate IDE (e.g., VSCode).
        
        3. The interface will prompt the user to input the name of the desired PDB file. Type in the full name of the file (along with the file path if not saved in the working directory) and press return to continue.

    .. code-block:: python

        >>> import ionerdss as ion
        >>> ion.PDB_UI()
        Enter pdb file name: ./tutorial/ReadPDBTutorial/1utc.pdb

    Once the file name is input, the code will read the desired information inside this PDB file and show some basic parameters on the interface (this will take a while), including the name of each chain, size of each chain, the coordinate of each COM and each pair of interfaces.

    .. code-block:: python

        Finish reading pdb file
        4 chain(s) in total: ['A', 'B', 'P', 'Q']
        Each of them has [2754, 2763, 66, 66] atoms.
        Center of mass of  A is: [0.975, 5.018, 3.545]
        Center of mass of  B is: [4.214, 6.886, 2.019]
        Center of mass of  P is: [2.635, 5.307, 3.115]
        Center of mass of  Q is: [2.555, 6.419, 2.222]
        Interaction site of A & B is: [1.752, 6.239, 2.643] and [2.223, 6.546, 2.559] distance between interaction sites is: 0.568 nm
        Interaction site of A & P is: [2.096, 5.612, 3.193] and [2.417, 5.159, 3.148] distance between interaction sites is: 0.557 nm
        Interaction site of A & Q is: [1.831, 5.940, 1.576] and [2.400, 6.433, 1.890] distance between interaction sites is: 0.815 nm
        Interaction site of B & P is: [3.350, 5.290, 2.839] and [2.856, 5.318, 3.063] distance between interaction sites is: 0.544 nm
        Interaction site of B & Q is: [3.064, 6.419, 1.962] and [2.619, 6.526, 2.028] distance between interaction sites is: 0.463 nm

    Among all pairs of interfaces, you will be prompted to change the distance between interfaces (also known as sigma). If you enter 'yes', you can modify any of the distances shown above or set all distances to the same value. If you enter 'no', the distances will remain unchanged.

    .. code-block:: python

        Would you like to change the distance between interaction site (Type 'yes' or 'no'): yes
        Which distance would you like to change (please enter an integer no greater than 5 or enter 0 to set all distance to a specific number): 0
        Please enter new distance: 1.5
        New interaction site of A & B is: [1.366, 5.987, 2.712] and [2.609, 6.798, 2.490] distance between new interaction sites is: 1.500 nm
        New interaction site of A & P is: [1.824, 5.995, 3.231] and [2.689, 4.776, 3.109] distance between new interaction sites is: 1.500 nm
        New interaction site of A & Q is: [1.593, 5.733, 1.445] and [2.639, 6.640, 2.021] distance between new interaction sites is: 1.500 nm
        New interaction site of B & P is: [3.785, 5.265, 2.642] and [2.421, 5.342, 3.260] distance between new interaction sites is: 1.500 nm
        New interaction site of B & Q is: [3.563, 6.298, 1.887] and [2.120, 6.647, 2.102] distance between new interaction sites is: 1.500 nm
        Would you like to change the distance between interaction site (Type 'yes' or 'no'): yes
        Which distance would you like to change (please enter an integer no greater than 5 or enter 0 to set all distance to a specific number): 1
        Please enter new distance: 1.5
        New interaction site of A & B is: [1.366, 5.987, 2.712] and [2.609, 6.798, 2.490] distance between new interaction sites is: 1.500 nm
        New interaction site of A & P is: [1.824, 5.995, 3.231] and [2.689, 4.776, 3.109] distance between new interaction sites is: 1.500 nm
        New interaction site of A & Q is: [1.593, 5.733, 1.445] and [2.639, 6.640, 2.021] distance between new interaction sites is: 1.500 nm
        New interaction site of B & P is: [3.785, 5.265, 2.642] and [2.421, 5.342, 3.260] distance between new interaction sites is: 1.500 nm
        New interaction site of B & Q is: [3.563, 6.298, 1.887] and [2.120, 6.647, 2.102] distance between new interaction sites is: 1.500 nm
        Would you like to change the distance between interaction site (Type 'yes' or 'no'): no
        Calculation is completed.
        Angles for chain A & B
        Theta1: 2.384, Theta2: 2.614, Phi1: -2.174, Phi2: 1.373, Omega: 1.175
        Angles for chain A & P
        Theta1: 1.359, Theta2: 0.520, Phi1: -1.433, Phi2: -1.715, Omega: -2.999
        Angles for chain A & Q
        Theta1: 1.595, Theta2: 1.189, Phi1: -3.008, Phi2: 0.491, Omega: 0.341
        Angles for chain B & P
        Theta1: 1.891, Theta2: 0.188, Phi1: -1.918, Phi2: -2.587, Omega: 1.817
        Angles for chain B & Q
        Theta1: 2.130, Theta2: 0.455, Phi1: -1.839, Phi2: -0.583, Omega: -1.870

    You can then choose to whether display the protein complex so far in a 3D plot. If you type “yes”, a 3D plot will be displayed showing the interfaces on all chains with updated changes of the distances between interfaces.

    .. code-block:: python

        Display a 3D plot of the protein complex? (Type 'yes' or 'no'): yes

    .. figure:: ./fig/ionerdss_pdb_ui.png
        :alt: Coarse-grained model of PDB 1utc
        :align: center
        :width: 80%

        The coarse-grained model of PDB 1utc.

    Finally, you will be asked if you want to center each chain at its Center of Mass (COM). If you choose 'yes', the COM coordinates will be normalized to (0,0,0), and the coordinates of all interfaces will be adjusted accordingly in the final output. If you choose 'no', the coordinates for all COMs and interfaces will remain unchanged. NERDSS simulation requires that the COM of each chain be at the origin.

    .. code-block:: python

        Do you want each chain to be centered at center of mass? (Type 'yes' or 'no'): yes
        COM is normalized as [0.000, 0.000, 0.000]
        Input files written complete.

    The code will then automatically quit and the corresponding input (multiple .mol files and single .inp file) will be found in the working directory.

- Jupyter notebook

    - **Description:** This notebook `read_pdb_tutorial <read_pdb_tutorial.html>`_ demonstrates how to convert a PDB file into a NERDSS input file, with the same functionality as `PDB_UI()`.