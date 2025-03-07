Input and Output Files of NERDSS
--------------------------------

MOL Files
~~~~~~~~~

The MOL format (`*.mol`) is used to store molecule template information for NERDSS. Each `*.mol` file corresponds to a specific molecule and must have a prefix that matches the molecule name used in the reactions defined in the INP file.

The MOL file contains essential properties of molecules, including their diffusion behavior, spatial configuration, and interaction sites. The following information can be specified:

- **Required**:

  - Molecule name (must match the name used in the INP file)

  - Initial copy number of the molecule

  - Translational diffusion constants

  - Rotational diffusion constants

  - Center of mass coordinates

  - At least one interface coordinate

- **Optional**:

  - Lipid designation (whether the molecule is a lipid)

  - Implicit lipid designation (if applicable)

  - Interface states

  - Pre-defined bonds

INP Files
~~~~~~~~~

The INP format (`*.inp`) is used for storing system information read by NERDSS, and the format is, as much as possible, shared with BioNetGenLanguage (BNGL) for model portability. It can be used for a new simulation or a restart simulation to change the simulation parameters or add new molecules and reactions to the previous system. The information in the `*.inp` file is stored in different blocks, which start with the `start` keyword and end with the `end` keyword. Four blocks are used: `parameters`, `boundaries`, `molecules`, and `reactions`. Molecules must be defined before reactions.

**Parameters Block**
^^^^^^^^^^^^^^^^^^^^

- **Required**:

  - Requested number of iterations

  - Timestep length

- **Optional**:

  - Interval to write timestep information

  - Interval to write to coordinates file

  - Interval to update the latest restart file

  - Interval to write separate restart files

  - Interval to write individual PDB files

**Boundaries Block**
^^^^^^^^^^^^^^^^^^^^

- **Required**: Water box dimensions

- **Optional**: `IsSphere`, radius of sphere

**Molecules Block**
^^^^^^^^^^^^^^^^^^
Includes the name and starting copy number of the molecules in the system, listed line by line. These should be consistent with the molecule name in the MOL files. Note that if the system has an implicit lipid molecule, it must be listed first.

**Reactions Block**
^^^^^^^^^^^^^^^^^^
Includes all the information about the reactions in the system.

Each reaction starts with a declaration like this:

.. code-block:: none

    A(a) + B(b) <-> A(a!1).B(b!1)

where `A` and `B` are the reacting molecules, and `a` and `b` are the reacting interfaces. `A(a!1).B(b!1)` is the product, where `!` denotes an interaction with index `1`, and `.` indicates the two molecules are interacting. Reversible reactions are denoted by a double-headed arrow `<->`. Interfaces must be uniquely named, at least on each molecule type. States are allowed and are not required to be binary, denoted with a tilde `~`. An interface can only change its state or interaction, not both.

Ancillary interfaces are allowed. These can include interfaces with/without states/interactions that do not change their state or interaction in the particular reaction but are required for the reaction to occur. For example, if a molecule `A` has two interfaces `a1` and `a2`, with `a2` having two states `P` and `U`, and an interaction between `a1` and some interface `b` on molecule `B` is dependent on `a2` being in the `P` state, we can write the reaction as:

.. code-block:: none

    A(a1,a2~P) + B(b) <-> A(a1!1,a2~P).B(b!1)

If an interaction between `a1` and some interface `b` on molecule `B` is dependent on `a2` being bound to something, we can write the reaction as:

.. code-block:: none

    A(a1,a2!*) + B(b) <-> A(a1!1,a2!*).B(b!1)

Here we use the wildcard `*` to represent ancillary interactions in the reactants. Another note is that wildcard states are allowed in the reactants/products by omitting the state of an interface that has states. If the state of an ancillary interface does not affect the reaction, it should not be listed. If it is listed, it will be required to be in the state listed.

Supported reaction types include:

- **Reversible binding reactions**:
  
  .. code-block:: none
  
     A(a) + A(a) <-> A(a!1).A(a!1)

- **Bimolecular association**:
  
  .. code-block:: none
  
     A(a) + B(b) -> A(a!1).B(b!1)

- **Bimolecular state change (enzyme-facilitated state change)**:
  
  .. code-block:: none
  
     A(a) + B(a~U) <-> A(a) + B(a~P)

- **Unimolecular state change**:
  
  .. code-block:: none
  
     A(a~S) -> A(a~O)

- **Dissociation**:
  
  .. code-block:: none
  
     A(a!1).B(b!1) -> A(a) + B(b)

- **Creation from concentration**:
  
  .. code-block:: none
  
     0 -> A(a)

- **Creation from molecule**:
  
  .. code-block:: none
  
     A(a) -> A(a) + B(b)

- **Destruction**:
  
  .. code-block:: none
  
     A(a) -> 0

Reaction Parameters
"""""""""""""""""""

The parameters for a reaction are given below the declaration line by line.

- **Required**:

  - 3D microscopic binding rate or macroscopic binding rate

  - Microscopic dissociation rate or macroscopic dissociation rate (only required for reversible reactions)

- **Optional**:

  - Distance between the two reacting interfaces for a bimolecular reaction (required for bimolecular association)

  - Angles for bimolecular association (required for bimolecular association)

  - Vector used to calculate the *phi1* and *phi2* angles (and sometimes *omega*)

  - Label for tracking the reaction product

DAT Files
~~~~~~~~~

NERDSS produces most of its output in the DAT format. DAT files with names ending in `_time.dat` contain system quantities as a function of time for a specific aspect.

The first line in these `_time.dat` files serves as a header, while the subsequent lines store data recorded at specified intervals. These intervals are defined in the `*.inp` file.

Below is a list of `_time.dat` files and their contents:

- **`observables_time.dat`**  

  - **Purpose**: Tracks time-dependent quantities of labeled observables specified in the `.inp` file’s reactions section.  

  - **Format**:  
   
    - The first line is a header listing observed labels.

    - Subsequent lines contain data recorded at intervals specified in the `.inp` file.  

- **`copy_numbers_time.dat`**  

  - **Purpose**: Records time-dependent copy numbers of all species (reactants and products).  

  - **Format**:  

    - **Header**:  

      - First column: `Time (s)`, followed by species names (comma-separated).  

    - **Examples**:  

      .. code-block:: none
          
          C(A1): Free A1 interface in molecule C
          C(A1!1).A(C1!1): A1-C1 bond between molecules C and A
      
    - **Data rows**: Time points with corresponding species counts.  

- **`histogram_complexes_time.dat`**  

  - **Purpose**: Tracks time-dependent composition and abundance of complexes.  

  - **Format**:  

    - Lines starting with `Time (s): [value]` mark a new time point.  

    - Subsequent lines list complexes and their compositions. Example:  

      .. code-block:: none

          22   C:3. A:2. B:5
      
      This means there are 22 complexes composed of 3 `C`, 2 `A`, and 5 `B` molecules.  

- **`mono_dimer_time.dat`**  

  - **Purpose**: Monitors monomers and perfect dimers (excludes dimers in larger complexes).  

  - **Format**:  

    - **Header**: `TIME (s)`, followed by `MONO:[name]` or `DIMERS W:[name]` (tab-separated).  

    - **Example**: Dimer counts for `A` (e.g., `AB + AC` dimers) are summed under `DIMERS W:A`.  

- **`bound_pair_time.dat`**  

  - **Purpose**: Tracks all directly bound pairs (e.g., `A-B` bonds) and system-wide loops.  

  - **Format**:  

    - **Header**: `TIME(s)`, followed by bound pair names (e.g., `C,A`) and `Nloops`.  

    - Additional columns track rejected/successful association events.  

- **`transition_matrix_time.dat`**  

  - **Purpose**: Logs transitions between cluster sizes (`n → m`) and tracks lifetimes of molecular sizes. 

  - **Structure**:  

    - **First half**: Transition matrix where:  

      - Diagonal = counts of unchanged cluster sizes.  

      - Off-diagonal = transitions between sizes.  

      - Row sums = total `n`-mers in the simulation.  
      
    - **Second half**: Lifetime data for each cluster size.  

  - **Parameters (set in `.mol` / `.inp` files)**:  

    - `countTransition`: Enable tracking (default: `false`).  

    - `transitionMatrixSize`: Matrix dimensions (default: `500`).  

    - `transitionWrite`: Output interval (default: `nItr/10`).  

Restart Files
~~~~~~~~~~~~~  

- **`restart.dat`**: Stores all system information needed to restart a simulation from the latest step.  

- **`rng_state`**: Stores the state of the Random Number Generator at the latest step. Required for debugging and ensuring the restarted trajectory follows the original path exactly. 

- **`restart$timeStep$.dat` and `rng_state$timeStep$`**:  

  - Contain information for restarting a simulation from a specific timestep.  

  - The interval for writing these files is determined by the `checkpoint` parameter in the `*.inp` file.  

  - Restarting a simulation is recommended in a new directory.  

XYZ Files
~~~~~~~~~

The XYZ format is used to store coordinates and trajectories generated by NERDSS. These files can be visualized using **VMD** and **Ovito**.

- **`initial_crds.xyz`**: Stores the initial coordinates of all molecules in the system.  

- **`final_coords.xyz`**: Stores the final coordinates of all molecules.  

- **`trajectory.xyz`**: Stores the full trajectory of the system.  

  - The interval for writing coordinates to this file is determined by the `trajWrite` parameter in the `*.inp` file.  

  - **Note**: If the total copy number of species changes per step (e.g., due to creation or destruction), these files may not work correctly in **VMD**.  

PSF Files
~~~~~~~~~

The PSF format is used for visualization in **VMD**. It defines:  

- Rigid molecules in the system.  

- Bonds between them.  

- The number of copies.  

⚠ **Limitation**: If the total number of species changes per step (e.g., due to creation or destruction), PSF files cannot be updated. In such cases, **PDB files with Ovito** should be used instead.  

PDB Files
~~~~~~~~~

The **PDB format** is an optional output for storing coordinates and trajectories in **NERDSS**.

Unlike **XYZ files**, which contain the entire trajectory in a single file, PDB output generates an **individual file for each frame**.

- **Advantages**:  

  - Compatible with **Ovito**.  

  - Does not require a fixed number of species per frame. 

  - Ideal for visualizing **open systems** where the total number of species can change.

Standard Output
~~~~~~~~~~~~~~~

NERDSS logs various details about the simulation system to standard output. This includes:

- Parsed information from input files

- Reactions occurring at each step

- Simulation time information at fixed intervals

- Warnings and error messages

This output helps in monitoring the simulation progress and diagnosing potential issues.

NERDSS Parameters
~~~~~~~~~~~~~~~~~

# is an indicator for comment. 

Parameters in MOL File
^^^^^^^^^^^^^^^^^^^^^^

The following parameters can be specified in a MOL file:

- **name**

  - **Acceptable Values**: String (required)

  - **Description**: The molecule name, which must match the name used in the INP file and be consistent with the MOL file name.

  - **Example**: `name = A`

- **isLipid**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Description**: Indicates if the molecule is restricted to a 2D surface (e.g., a lipid or transmembrane protein).

  - **Example**: `isLipid = true`

- **isImplicitLipid**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Description**: Indicates if the molecule is an implicit lipid, used for simulating binding to a membrane with many lipid binding sites.

  - **Example**: `isImplicitLipid = true`

- **checkOverlap**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Description**: Specifies if steric overlap is checked during association for this molecule type.

  - **Example**: `checkOverlap = true`

- **countTransition**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Description**: Indicates if size transition is counted during simulation for this molecule type.

  - **Example**: `countTransition = true`

- **transitionMatrixSize**

  - **Acceptable Values**: Integer (optional)

  - **Default Value**: `500`

  - **Description**: The size of the transition matrix.

  - **Example**: `transitionMatrixSize = 100`

- **insideCompartment**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Description**: Indicates if this molecule type is inside the compartment.

  - **Example**: `insideCompartment = true`

- **outsideCompartment**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Description**: Indicates if this molecule type is outside the compartment.

  - **Example**: `outsideCompartment = true`

- **D**

  - **Acceptable Values**: Array [x, y, z] (required)

  - **Description**: The molecule’s translational diffusion constants in the x, y, and z directions.

  - **Unit**: µm²/s

  - **Example**: `D = [25.0, 25.0, 25.0]`

- **Dr**

  - **Acceptable Values**: Array [x, y, z] (required)

  - **Description**: The molecule's rotational diffusion constants in the x, y, and z directions.

  - **Unit**: rad²/µs

  - **Example**: `Dr = [0.5, 0.5, 0.5]`

- **COM**

  - **Acceptable Values**: Coordinates block (required)

  - **Description**: The center-of-mass (COM) coordinates and all interface coordinates. Interface names must match those used in the INP file.

  - **Unit**: nm

  - **Example**:

    .. code-block:: none

        COM             0.0  0.0  0.0
        interfaceName1  0.0  0.0  1.5
        interfaceName2  0.0  0.0 -1.5

- **bonds**

  - **Acceptable Values**: Bonds block (optional)

  - **Description**: Bonds for the molecule, declared for visualization purposes. The first line specifies the number of bonds, followed by pairs of interface names.

  - **Example**:

    .. code-block:: none

        bonds = 2
        interfaceName1
        interfaceName2

- **state**

  - **Acceptable Values**: Single character (optional)

  - **Description**: Defines interface states with the format `interfaceName~X~Y`, consistent with the name used in the INP file.

  - **Example**: `state = interfaceName1~P~U`

- **mass**

  - **Acceptable Values**: Float (optional)

  - **Default Value**: Calculated from the molecule radius, which is determined by the largest distance from the COM to interfaces.

  - **Description**: Used to determine the geometric center of mass of a multi-component complex. Rotation occurs relative to this COM. Mass is effectively unitless, as total mass is divided out.

  - **Example**: `mass = 1`

Parameters in INP File
^^^^^^^^^^^^^^^^^^^^^^

**Parameters Block** (between `start parameters` and `end parameters`):

- **nItr**

  - **Acceptable Values**: Integer (required)

  - **Description**: Requested number of iterations.

  - **Example**: `nItr = 10000`

- **timeStep**

  - **Acceptable Values**: Float (required)

  - **Description**: Timestep length per iteration.

  - **Unit**: µs

  - **Example**: `timeStep = 0.1`

- **timeWrite**

  - **Acceptable Values**: Integer (optional)

  - **Default Value**: 10

  - **Description**: Iteration interval to print running time information to standard output and to record the copy numbers in the `_time.dat` files.

  - **Example**: `timeWrite = 100`

- **trajWrite**

  - **Acceptable Values**: Integer (optional)

  - **Default Value**: 10

  - **Description**: Iteration interval to write coordinates to the trajectory file.

  - **Example**: `trajWrite = 100`

- **restartWrite**

  - **Acceptable Values**: Integer (optional)

  - **Default Value**: 10

  - **Description**: Iteration interval to write restart files.

  - **Example**: `restartWrite = 100`

- **pdbWrite**

  - **Acceptable Values**: Integer (optional)

  - **Default Value**: -1

  - **Description**: Iteration interval to write PDB files; `-1` means no PDB file output.

  - **Example**: `pdbWrite = 100`

- **checkPoint**

  - **Acceptable Values**: Integer (optional)

  - **Default Value**: `nItr / 10`

  - **Description**: Iteration interval to write checkpoint for restart.

  - **Example**: `checkPoint = 1000`

- **transitionWrite**

  - **Acceptable Values**: Integer (optional)

  - **Default Value**: `nItr / 10`

  - **Description**: Iteration interval to write the transition matrix.

  - **Example**: `transitionWrite = 1000`

- **clusterOverlapCheck**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Description**: Indicates if overlap is checked based on the cluster.

  - **Example**: `clusterOverlapCheck = true`

- **overlapSepLimit**

  - **Acceptable Values**: Float (optional)

  - **Default Value**: 0.1

  - **Description**: COM-COM distance less than this value is canceled for molecules whose `checkOverlap` is `true`.

  - **Unit**: nm

  - **Example**: `overlapSepLimit = 3.0`

- **scaleMaxDisplace**

  - **Acceptable Values**: Float (optional)

  - **Default Value**: 100.0

  - **Description**: Association events resulting in shifts of an interface on either component by `scaleMaxDisplace * <RMSD>` are rejected. `<RMSD>` is calculated from `sqrt(6.0 * Dtot * dt)` in 3D, and `sqrt(4.0 * Dtot * dt)` in 2D.
  
  - **Unit**: nm

  - **Example**: `scaleMaxDisplace = 10.0`

**Boundaries Block** (between `start boundaries` and `end boundaries`):

- **WaterBox**

  - **Acceptable Values**: Array [x, y, z] (required)

  - **Description**: The XYZ dimensions of the simulation system.

  - **Unit**: nm

  - **Example**: `WaterBox = [500.0, 500.0, 500.0]`

- **xBCtype/yBCtype/zBCtype**

  - **Acceptable Values**: `reflect` (optional)

  - **Default Value**: `reflect`

  - **Description**: The boundary conditions for each dimension.

  - **Example**:

    .. code-block:: none

        xBCtype = reflect
        yBCtype = reflect
        zBCtype = reflect

- **isSphere**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Example**: `isSphere = false`

- **sphereR**

  - **Acceptable Values**: Float (optional)

  - **Default Value**: 0

  - **Unit**: nm

  - **Example**: `sphereR = 1000`

- **hasCompartment**

  - **Acceptable Values**: Boolean (optional)

  - **Default Value**: `false`

  - **Example**: `hasCompartment = true`

- **compartmentR**

  - **Acceptable Values**: Float (optional)

  - **Default Value**: 0

  - **Unit**: nm

  - **Example**: `compartmentR = 1000`

- **compartmentSiteD**

  - **Acceptable Values**: Float (optional)

  - **Default Value**: 0

  - **Unit**: nm²/µs

  - **Example**: `compartmentSiteD = 10.0`

- **compartmentSiteRho**

  - **Acceptable Values**: Float (optional)

  - **Default Value**: 0

  - **Unit**: nm⁻²

  - **Example**: `compartmentSiteRho = 10.0`

**Molecules Block** (between `start molecules` and `end molecules`):

This block includes all the molecule types in the simulation system and their starting copy numbers. The names of the molecules should be consistent with the corresponding `.mol` files. If an implicit lipid molecule exists, it must be listed first.

- **Example**:

  .. code-block:: none

      ImplicitLipid : Ncopies
      moleculeName1 : Ncopies
      moleculeName2 : Ncopies

If a molecule has more than one state, those can be initialized with distinct copy numbers. For example, molecule `Kinase` with site `a` will be initialized with 100 copies in state `P`, and 200 copies in state `U`.

- **Example**:

  .. code-block:: none

      Kinase : 100 (a~P), 200 (a~U)

For a molecule `pip2` that has two sites `head` and `tail`, each of which can exist in 2 states (`head~U~P` and `tail~S~D`):

- **Example**:

  .. code-block:: none

      pip2 : 60 (head~U, tail~S), 10 (head~P, tail~D), 10 (head~U, tail~D), 10 (head~P, tail~S)

**Reactions Block** (between `start reactions` and `end reactions`):

Each reaction starts with a declaration followed by the corresponding parameter values for this reaction. The syntax of the declaration and the supported reaction types are given in the INP files section. Here is the description of the parameters for each reaction.

- **onRate3Dka**

  - **Acceptable Values**: Float (one of `onRate3Dka` and `onRate3DMacro` must be provided)

  - **Description**: 3D microscopic binding rate.

  - **Unit**: nm³/µs (for 2D, converted to nm²/µs by `length3Dto2D`; for creation: M/s)

  - **Example**: `onRate3Dka = 1.0`

- **onRate3DMacro**

  - **Acceptable Values**: Float (one of `onRate3Dka` and `onRate3DMacro` must be provided)

  - **Description**: Macroscopic binding rate. The relationship between 3D microscopic binding rate and macroscopic binding rate for different systems can be found in the supporting information of the NERDSS paper.
  
  - **Unit**: µM⁻¹s⁻¹ (1 µM⁻¹s⁻¹ = 1/0.602214076 nm³/µs)

  - **Example**: `onRate3DMacro = 1.0`

- **offRatekb**

  - **Acceptable Values**: Float (one of `offRatekb` and `offRateMacro` must be provided for reversible reactions)
  
  - **Description**: Microscopic dissociation rate.
  
  - **Unit**: s⁻¹
  
  - **Example**: `offRatekb = 1.0`

- **offRateMacro**
  
  - **Acceptable Values**: Float (one of `offRatekb` and `offRateMacro` must be provided for reversible reactions)
  
  - **Description**: Macroscopic dissociation rate. The relationship between microscopic dissociation rate and macroscopic dissociation rate for different systems can be found in the supporting information of the NERDSS paper.
  
  - **Unit**: s⁻¹
  
  - **Example**: `offRateMacro = 1.0`

- **rate**
  
  - **Acceptable Values**: Float
  
  - **Description**: Used for zeroth and first-order reactions. If used for bimolecular reactions, it maps to `onRate3Dka`.
  
  - **Unit**: Reaction order dependent: Zeroth (M/s), First (1/s)
  
  - **Example**: `rate = 10.0`

- **sigma**
  
  - **Acceptable Values**: Float (optional)
  
  - **Default Value**: 1.0
  
  - **Description**: Distance between the two reacting interfaces for a bimolecular reaction.
  
  - **Unit**: nm
  
  - **Example**: `sigma = 1.0`

- **norm1/norm2**
  
  - **Acceptable Values**: Vector (optional)
  
  - **Default Value**: [0, 0, 1]
  
  - **Description**: Vectors used to calculate the phi and phi2 angles (and sometimes omega) for a bimolecular reaction. Definitions can be found in the supporting information of the NERDSS paper. norm1 and norm2 are relative to the molecule template orientation. when calculating the binding angles using formulae in the NERDSS paper, the vectors are needed to rotated to the real orientation of the molecule.
  
  - **Example**: 
    
    .. code-block:: none

        norm1 = [0, 0, 1]
        norm2 = [0, 0, 1]

- **assocAngles**

  - **Acceptable Values**: Vector (optional)

  - **Default Value**: [nan, nan, nan, nan, nan]

  - **Description**: Five angles for bimolecular association. Definitions can be found in the supporting information of the NERDSS paper. If an angle does not exist, it should be `nan`. `M_PI` is Pi (3.14159). For all `nan`, the binding partners are placed at the orientation they were prior to the association event.
  
  - **Unit**: rad
  
  - **Example**: `assocAngles = [1.5707963, 1.5707963, nan, nan, M_PI]`

- **length3Dto2D**

  - **Acceptable Values**: Float (optional)
  
  - **Default Value**: 2 * sigma
  
  - **Description**: Length scale to convert 3D rate to 2D rate.
  
  - **Unit**: nm
  
  - **Example**: `length3Dto2D = 30`

- **bindRadSameCom**

  - **Acceptable Values**: Float (optional)
  
  - **Default Value**: 1.1
  
  - **Description**: Scalar multiple of sigma, determines the distance between two reactants to force reaction within the same complex.
  
  - **Unit**: Unitless
  
  - **Example**: `bindRadSameCom = 1.1`

- **loopCoopFactor**

  - **Acceptable Values**: Float (optional)
  
  - **Default Value**: 1.0
  
  - **Description**: Multiplies the rate by this scale factor, used only when closing loops, such as within a hexagonal lattice. `lCF = exp(-∆Gcoop/kBT)`.
  
  - **Unit**: Unitless
  
  - **Example**: `loopCoopFactor = 0.001`

- **observeLabel**

  - **Acceptable Values**: String (optional)
  
  - **Description**: Label for tracking the reaction product. The copy numbers of each `observeLabel` are stored in `observables_time.dat`.
  
  - **Example**: `observeLabel = leg`

- **rxnLabel**
  
  - **Acceptable Values**: String (optional)
  
  - **Description**: Name for the reaction. Helpful for coupling a different reaction to this one.
  
  - **Example**: `rxnLabel = phosphorylateA`

- **coupledRxnLabel**
  
  - **Acceptable Values**: String from `rxnLabel` (optional)
  
  - **Description**: Allows the completion of a reaction to immediately cause another reaction to happen. The triggered reaction must already be listed and will occur with the rate `kcat` (if specified). Only applies to products of a reaction and couples currently to dissociation only.
  
  - **Example**: `coupledRxnLabel = phosphorylateA`

- **kcat**
  
  - **Acceptable Values**: Float (optional)
  
  - **Description**: For a `coupledRxn`, will occur with this rate. Only used if `coupledRxnLabel` is specified. Useful for Michaelis-Menten reactions.
  
  - **Unit**: s⁻¹
  
  - **Example**: `kcat = 1.0`

- **excludeVolumeBound**
  
  - **Acceptable Values**: Boolean (optional)
  
  - **Default Value**: `false`
  
  - **Description**: Once two sites are in the bound state, they will not try to bind and therefore will not exclude volume with any other sites.
  
  - **Example**: `excludeVolumeBound = false`