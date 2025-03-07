Parallel NERDSS
~~~~~~~~~~~~~~~~

The MPI implementation of the simulator leverages distributed computing techniques to divide the simulation workload across multiple processors and nodes.

Domain Decomposition
^^^^^^^^^^^^^^^^^^^^

a) The simulation volume is partitioned along the x-axis, with each partition assigned to a distinct processor.
b) Each processor is responsible for a subset of the sub-volumes within its assigned region.
c) A processor corresponds to a single MPI rank.

Processor Topology
^^^^^^^^^^^^^^^^^^

a) Processors are arranged in a linear topology along the x-axis.
b) For any given processor n:
    • If there is an adjacent processor on its left side, it is referred to as the “left neighbor processor”, n-1.
    • Similarly, an adjacent processor on the right side is called the “right neighbor processor”, n+1.

Edge and Ghost Regions
^^^^^^^^^^^^^^^^^^^^^^

a) Edge Region: For a processor with a neighbor on one side, the sub-volumes at the boundary along the x-axis are designated as the “Edge region”. The Edge region contains all the molecules that may interact with molecules in the neighboring processor’s domain.
b) Ghost Region: A copy of a neighboring processor’s Edge region. Thus, these sub-volumes are not owned by the processor. Ghost regions ensure the evaluation of reactions that occur across processor boundaries.
c) The update of Ghost and Edge regions during the simulation is implemented using Message Passing Interface (MPI) functions.

Extended Properties for Molecules and Complexes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To facilitate efficient parallel processing and inter-processor communication, we introduce additional properties to the Molecule and Complex classes.

a) Global ID: Since each processor maintains its own local indexing system for molecules and complexes, global unique IDs ensure unambiguous identification of entities throughout the distributed simulation environment.
b) Spatial Region Flags: Four Boolean properties are added to both Molecule and Complex on each processor:
    i. isLeftGhost: True for a complex if any part of it is in the left Ghost region. True for a molecule in the left Ghost region. True for a molecule that is part of a complex in the left Ghost region, and that molecule is not in the left Edge region.
    ii. isLeftEdge: True for a complex if any part of it is in the left Edge region. True for a molecule in the left Edge region. True for a molecule that is part of a complex in the left Edge region, and that molecule is not in the left Ghost region.
    iii. isRightEdge: Same conditions as above.
    iv. isRightGhost: Same conditions as above.
c) Region Assignment Consequences:
    i. Molecules can only be ‘True’ for one of these four regions, or ‘False’ for all of them.
    ii. Complexes can be ‘True’ for two regions if they span both an Edge and Ghost region.
    iii. Every single molecule in a Complex that has a ‘True’ flag will either be assigned as a Ghost or Edge molecule. This includes molecules that extend out of both the ghost and edge sub-volumes. These molecules must be assigned a sub-volume on the physical processor, even though molecules beyond the ghost region exist outside of it. They are assigned to the closest sub-volume by retaining the y and z index of the sub-volume, and setting the x index to 0.
d) Communication Tracking: A Boolean property receivedFromNeighbor is added to both Molecule and Complex classes. This property is used to track the loss of molecules and complexes from the observed processor during the inter-processor communication.
e) Communication Protocol:
    i. Before communication: receivedFromNeighbor is set to false for all molecules and complexes in Edge and Ghost regions.
    ii. After receiving data from a neighbor processor: receivedFromNeighbor is set to true for all received entities.
    iii. Post-communication cleanup: Any molecule or complex in Edge or Ghost regions with receivedFromNeighbor == false is considered not received back from the neighbor and is deleted from the current processor.

Pseudo-code for Parallel NERDSS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Initialization:
    1.1 Initialize simulation domain and parameters

    1.2 Partition simulation volume along x-axis

    1.3 Assign partitions to available processors

2. Pre-Process Setup:
    For each processor:
        2.1 Initialize local sub-volumes, moleculeList, and complexList

        
        2.2 Assign global IDs to molecules and complexes
        
        2.3 Identify Edge regions based on the sub-volume indices

            - If sub-volume x-index is 1, it is a left edge

            - If sub-volume x-index is N-2, it is a right edge

            - x-index 0 for the left ghost-region

            - x-index N-1 for the right ghost-region

        2.4 Set spatial region flags for molecules and complexes

3. Main Simulation Loop:
    For each time step:
        
        3.1 Process Local Reactions:
            
            3.1.1 Perform zeroth-order and first-order reactions
                - Exclude right edge region

                - Include left ghost region

                - Exclude right ghost region

            3.1.2 Perform second-order bimolecular reactions
                - Include left and right edge regions

                - Include left and right ghost regions

        3.2 Divide Processor Region:
            - Split physical region into Left half and Right half

            - Create left half list and right half list

        3.3 Process Left Half:
            
            3.3.1 Perform second-order bimolecular reactions
                - Include left ghost region

                - Set isAssociated flag if molecule associates

            3.3.2 Diffuse unreacted complexes
                - Exclude left ghost region

                - Do not diffuse complexes spanning left/right half

            3.3.3 Update sub-volume memberships and spatial region flags

        3.4 Left-to-Right Communication:
            - Set receivedFromNeighbor to false for right edge and ghost regions

            
            - Send left edge and ghost data to left neighbor processor
            
            - Receive data from right neighbor processor
            
            - Update right ghost and edge regions
            
            - Delete unreceived molecules and complexes in right ghost/edge regions

        3.5 Process Right Half:
            
            3.5.1 Perform second-order bimolecular reactions
                - Exclude molecules that diffused into right half
                
                - Exclude right edge and ghost regions
            3.5.2 Diffuse unreacted complexes
                - Include right half and right edge region
                
                - Handle complexes spanning edge and ghost regions

            3.5.3 Update sub-volume memberships and spatial region flags

        3.6 Right-to-Left Communication:
            - Set receivedFromNeighbor to false for left edge and ghost regions
            
            - Send right edge and ghost data to right neighbor processor
            
            - Receive data from left neighbor processor
            
            - Update left ghost and edge regions
            
            - Delete unreceived molecules and complexes in left ghost/edge regions

        3.7 Post-Processing:
            
            3.7.1 Reset reaction information for all molecules
            
            3.7.2 Update sub-volume memberships and spatial region flags
            
            3.7.3 Update simulation time and collect data

4. Finalization:
    
    4.1 Merge results from all processors
    
    4.2 Generate final output

Parallel NERDSS Communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Messaging Functions
"""""""""""""""""""

Distributing the initial data among ranks and updating between ranks is performed by **MPI messaging**. Packing and unpacking the data for communication is performed by **serialization** and **deserialization** routines. Due to the large number of disparate and nested structures, the use of **MPI derived types** (containers with descriptive formatting) was considered an unnecessary complication.

Serialization of an object **converts its data into a single array of raw bytes**, so that:

- It can be transferred over the network in a single MPI transfer.

- It can be stored in a binary file for checkpointing.

- Only mutable fields are transferred, avoiding unnecessary data.

Deserialization is the opposite process. It **restores objects from raw data** received through the network (or from a file). Since serialization and deserialization are **bitwise copy procedures**, structures with substructures must be processed **recursively**. That is, objects contained in an object are serialized (and deserialized) separately.

Serialization Mechanism
"""""""""""""""""""""""

APIs exist for each type of structure, including **templated forms** for lists, maps, and other containers. This **component-based approach** simplifies adding new structures for serialization.

### Storing Data in ``arrayRank``

The serialized (packed) data are stored in an array of bytes (``arrayRank``) and sent as a **single object** to another rank. The suffix **"Rank"** in variable names indicates that the data is intended for another rank.

### Example: Storing a Primitive Variable

A primitive type, such as a ``double`` variable ``x``, is stored in ``arrayRank`` at byte zero:

.. code-block:: cpp

    *( (double *) &(arrayRank[0]) ) = x;

To store the next object in ``arrayRank`` at the next empty byte:

.. code-block:: cpp

    *( (double *) &(arrayRank[sizeof(double)]) ) = y;

To keep track of the next free position in ``arrayRank``, an integer ``nArrayRank`` is used:

.. code-block:: cpp

    *( (double *) &(arrayRank[nArrayRank]) ) = y;
    nArrayRank += sizeof(double);

At the end of serialization, ``nArrayRank`` contains the total **size of ``arrayRank`` that needs to be sent**.

Deserialization Mechanism
"""""""""""""""""""""""""

Deserialization reverses the process by **extracting stored values** from ``arrayRank``. The value for ``y`` is retrieved as follows:

.. code-block:: cpp

    y = *( (double *) &(arrayRank[nArrayRank]) );
    nArrayRank += sizeof(double);

After all objects have been deserialized, ``nArrayRank`` contains the total occupied storage size.

Template-Based Serialization for Containers
"""""""""""""""""""""""""""""""""""""""""""

Serialization functions can be **generalized** for any base type using **C++ templates**.

### Template Function for Serializing a Primitive Vector

.. code-block:: cpp

    template <typename T>
    void serialize_primitive_vector(std::vector<T> to_serialize, unsigned char *arrayRank, int &nArrayRank);

Example usage:

.. code-block:: cpp

    serialize_primitive_vector<int>(emptyMolList, arrayRank, nArrayRank);

### Template Function for Deserializing a Primitive Vector

.. code-block:: cpp

    template <typename T>
    void deserialize_primitive_vector(std::vector<T> &to_deserialize, unsigned char *arrayRank, int &nArrayRank);

Example usage:

.. code-block:: cpp

    deserialize_primitive_vector<int>(emptyMolList, arrayRank, nArrayRank);

Serialization for Matrices
"""""""""""""""""""""""""""

Serialization and deserialization functions are also available for **matrices**:

### Template Function for Serializing a Matrix

.. code-block:: cpp

    template <typename T>
    void serialize_primitive_matrix(std::vector< std::vector<T> > to_serialize, unsigned char *arrayRank, int &nArrayRank);

### Template Function for Deserializing a Matrix

.. code-block:: cpp

    template <typename T>
    void deserialize_primitive_matrix(std::vector< std::vector<T> > &to_deserialize, unsigned char *arrayRank, int &nArrayRank);

Serialization for Vector-of-Arrays
"""""""""""""""""""""""""""""""""""

Containers requiring a **size type** can be serialized with a slight modification:

.. code-block:: cpp

    template <typename T, std::size_t S>
    void serialize_vector_array(std::vector< std::array<int, S> > to_serialize, unsigned char *arrayRank, int &nArrayRank);

Example usage:

.. code-block:: cpp

    serialize_vector_array<int, 3>(crossrxn, arrayRank, nArrayRank);

Matrices are serialized and deserialized using the following template functions:

.. code-block:: cpp

    template <typename T>
    void serialize_abstract_matrix(std::vector< std::vector<T> > to_serialize, unsigned char *arrayRank, int &nArrayRank);

.. code-block:: cpp

    template <typename T>
    void deserialize_abstract_matrix(std::vector< std::vector<T> > &to_deserialize, unsigned char *arrayRank, int &nArrayRank);

Custom Serialization Functions
"""""""""""""""""""""""""""""""

If additional serialization functions are needed, developers should first check existing implementations before creating a new one. If a new function must be added, **follow the naming conventions** used in the template functions.

Serializing and Deserializing Macros
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the previous section, the **serializing/deserializing functions** were described by their basic operation:  
- Packing data into an **array of bytes** (``arrayRank``).  

- Recording the **total number of occupied bytes** of the array in ``nArrayRank``.  

We illustrate the serialization operation again for an integer ``x``:

.. code-block:: cpp

    *( (int *) &(arrayRank[nArrayRank]) ) = x;
    nArrayRank += sizeof(int);

The complicated syntax of the first statement **hides the simplicity** of the bitwise copy operation and may be difficult to read for those unfamiliar with **casting variables** into different types.


Macros for Simplified Serialization
"""""""""""""""""""""""""""""""""""

To regain **simplicity and readability**, **macros** are introduced.  
The **PUSH(variable)** macro is a **single-argument macro** used to **serialize** a primitive type.  
It generalizes serialization to work with **all primitive types**.

Instead of manually writing:

.. code-block:: cpp

    *( (int *) &(arrayRank[nArrayRank]) ) = x;
    nArrayRank += sizeof(int);

We can **replace this with a macro** that automatically determines the **type and size** of the variable.

### **Definition of PUSH(variable) Macro**
The macro uses **``__typeof__``** to let the compiler determine the type and size of the argument.

.. code-block:: cpp

    #define PUSH(variable) \
    *( (__typeof__ (variable) *) (arrayRank + nArrayRank) ) = variable; \
    nArrayRank += sizeof(variable);

- ``arrayRank`` and ``nArrayRank`` are **assumed to be in scope**.

- The **type and size** of the argument are extracted using **``__typeof__``** and **``sizeof``**.


Macros for Deserialization
"""""""""""""""""""""""""""

Similarly, **deserialization** retrieves values from ``arrayRank`` into a variable.  
The **POP(variable)** macro extracts a primitive type **from** ``arrayRank`` starting at ``nArrayRank`` and updates ``nArrayRank`` accordingly.

### **Definition of POP(variable) Macro**
.. code-block:: cpp

    #define POP(variable) \
    variable = *( (__typeof__ (variable) *) (arrayRank + nArrayRank) ); \
    nArrayRank += sizeof(variable);

This makes deserialization **simpler and more readable** compared to manually extracting values.

Usage of PUSH and POP Macros
"""""""""""""""""""""""""""""

The following examples demonstrate how **PUSH** and **POP** are used for serializing and deserializing **primitive type variables**.

#### **Example 1: Serializing and Deserializing an Integer**
.. code-block:: cpp

    int a;
    PUSH(a);  // Serialize variable 'a'

    ...

    int b;
    POP(b);   // Deserialize into 'b'

#### **Example 2: Serializing an Expression**
.. code-block:: cpp

    PUSH(15 + 4);  // Stores the result of (15 + 4)

Auxiliary Structures for Parallel Execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``MpiContext`` structure is a container for most of the data related to **parallel execution**.  
This is the **only parallel structure** passed as a **single, final argument** to many functions.

A **single parallel container object** is used instead of multiple individual structures because:
- The **serial simulator** has deep **call stacks** (up to 10 levels of nested function calls).
- Propagating various parallelization structures through the **function chain** would require **substantial modification** to argument lists.
- Using a **single argument container** prevents future argument list changes in parallelization modifications.
- Developers can **easily identify** functions that support parallel execution when they see an ``mpiContext`` argument.

While ``MpiContext`` is **unique per rank**, it could be defined as a **global variable** to avoid modifying serial function declarations.  
However, using **global variables is discouraged** for maintainability.

---

MpiContext Structure Definition
"""""""""""""""""""""""""""""""

The following code defines ``MpiContext`` as a **typedef** for ``structMpiContext``:

.. code-block:: cpp

    typedef struct structMpiContext {  // Holds MPI-related data
        ...
    } MpiContext;

### **Rank Number and Size**
The rank number and total number of MPI processes are stored in ``rank`` and ``nprocs``:

.. code-block:: cpp

    int nprocs;  // Number of MPI processes
    int rank;    // MPI rank number

These values are used to:
- **Determine neighboring ranks** for shared zones.
- **Identify ranks** involved in shared complexes.

### **Simulation Iteration Number**
The current **simulation iteration number** is stored in ``mpiContext``.  
This allows debugging with **print statements** after a certain number of iterations:

.. code-block:: cpp

    int simItr;

---

Pointers to Serial Data Structures
"""""""""""""""""""""""""""""""""""

The ``mpiContext`` structure **encapsulates pointers** to key simulation components:

.. code-block:: cpp

    Membrane *membraneObject;
    SimulVolume *simulVolume;
    std::vector<Molecule> *moleculeList;
    std::vector<Complex> *complexList;

These pointers enable **parallel processing and debugging**.

---

MPI Communication Buffers
"""""""""""""""""""""""""

The following fields **store pointers** to byte arrays (``MPIArray`` buffers) for  
**Send/Recv operations** between left and right ranks:

.. code-block:: cpp

    unsigned char* MPIArrayToRight;
    unsigned char* MPIArrayFromRight;
    unsigned char* MPIArrayToLeft;
    unsigned char* MPIArrayFromLeft;

Array **position indicators** and **storage size**:

.. code-block:: cpp

    int nMPIArrayToRight;
    int nMPIArrayFromRight;
    int nMPIArrayToLeft;
    int nMPIArrayFromLeft;
    int sendBufferSize, recvBufferSize;

### **Memory Allocation Behavior**
- The **MPI arrays** are allocated dynamically using ``malloc``.
- If usage **approaches capacity**, the buffer size **increases by 20%**.

---

MPI Send/Recv Synchronization
"""""""""""""""""""""""""""""

Non-blocking **MPI_Request identifiers** and **MPI_Status objects** are used  
to **track outstanding Send/Recv operations**:

.. code-block:: cpp

    // Non-blocking identifiers for synchronization
    MPI_Request requestSendToLeft, requestSendToRight;
    MPI_Request requestRecvFromLeft, requestRecvFromRight;
    
    // Contains byte count and status information
    MPI_Status statusRecvFromLeft, statusRecvFromRight;

---

Rank-Specific Binning Offsets
"""""""""""""""""""""""""""""

Each rank maintains a **binning offset**, ``xOffset``, to determine its **local x-bin**.

### **Function to Compute Local X-Bin**
.. code-block:: cpp

    int xOffset;
    inline int get_x_bin(MpiContext &mpiContext, Molecule &mol) {
        return int(
            (mol.comCoord.x + (*(mpiContext.membraneObject)).waterBox.x / 2) /
            (*(mpiContext.simulVolume)).subCellSize.x
        ) - mpiContext.xOffset;
    }

#### **Explanation:**

- The molecule’s **x-coordinate** is adjusted from **[-X/2, X/2]** to **[0, X]**.

- It is **divided by cell size** to get a **global x-bin number**.

- The **``xOffset`` adjustment** ensures **local bin numbers start at 0**.

### **Handling Uneven Bin Distributions**
When ``nprocs`` does not evenly divide the total bins, the **remaining bins**  
are distributed across the **lowest-rank processes**.

Example **distribution for 12 bins across 5 ranks**:
``3, 3, 2, 2, 2``

**xOffsets for ranks {0,1,2,3,4}:**  
``{0, 3, 6, 8, 10}``

---

Defining Start and Ghost Zones
"""""""""""""""""""""""""""""""

The following fields define **owned (shared) zones** and **ghost zones**:

.. code-block:: cpp

    int startCell, endCell;        // First and last owned zones
    int startGhosted, endGhosted;  // First and last ghost zones

---

MPI Buffer Space Considerations
"""""""""""""""""""""""""""""""

Currently, some **"magic number" constants** are used for the **communication buffers**.  
These are set high to **handle worst-case scenarios** but may need adjustment  
at **larger scales**.

- **Communication buffers are self-growing**, but their **initial values must be large enough**.

- If **scaling changes**, the **initial values may fail** for the **first iteration**.

Preparing Data Structures for Parallel Execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A significant portion of the code is dedicated to **ingesting user input**, but this process  
consumes an **insignificant amount of total execution time**. To **preserve the serial code**,  
**only rank 0** parses the input, as if executing in serial mode.

### **Role of Rank 0 in Data Preparation**

- **Rank 0** holds the **entire dataset** (molecules, complexes, cells, etc.).

- **Rank 0 partitions the dataset** into **rank-specific subsets** for distributed execution.

- Some **new fields** have been introduced in these data structures, which are **parallel-specific**  
  and **irrelevant for serial execution**.

---

Molecule Indexing in Parallel Execution
"""""""""""""""""""""""""""""""""""""""

Initially, a **Molecule structure** exists for **every molecule**, with a **unique index**  
(``Molecule.index``) referring to its position in the **serial** ``moleculeList`` vector.

- **Serial execution:**  
  
  - Molecule indices range from ``0`` to ``Nall-1``, where ``Nall`` is the total number of molecules.

- **Parallel execution:**  
  
  - Each rank contains a **subset of molecules**, indexed from ``0`` to ``Nrank-1``.
  
  - ``Nrank`` is the number of molecules in a rank’s subset.
  
  - The **sum of all rank-specific molecule counts**:  
    ``sum(Nrank) = Nall``

To **uniquely identify molecules across ranks**, a **global identifier** is assigned:

- **Local index** → Used within a rank for looping in serial functions.

- **Global ID** → Used to uniquely track molecules across ranks.

For convenience, **mapping arrays** are created to **convert between rank-specific indices and global IDs**:

.. code-block:: cpp

    mapSerialToParallelMolecule  // Maps serial index to rank-specific index
    mapParallelToSerialMolecule  // Maps rank-specific index to global ID

These **maps exist only during data partitioning**.

---

Data Partitioning
""""""""""""""""""

The **partitioning process** involves selecting molecules, complexes, and cells from  
the **serial-specific** lists and placing them into **rank-specific** lists:

.. code-block:: cpp

    moleculeList      → moleculeListRank  (Rank-specific molecules)
    complexList       → complexListRank   (Rank-specific complexes)
    subCellList       → subCellListRank   (Rank-specific cells)

Each **rank-specific structure** contains:
1. **Copied data from the original serial structure**.
2. **Modified indices** for parallel execution.
3. **Parallel-specific fields** set with appropriate values.

For consistency, **rank-specific lists** retain their **original names** but with a **Rank suffix**.  
Example: ``moleculeListRank`` (rank-specific list), ``complexListRank`` (rank-specific list).

---

Simulation Volume and Cells
"""""""""""""""""""""""""""

The **simulation volume** consists of **nested hierarchical structures**:

- **Simulation volume** → The cubic box where the simulation occurs.

- **Subvolumes (cells)** → Divisions of the simulation volume into equal parts.

### **Simulation Volume Definitions**
.. code-block:: cpp

    WaterBox.x, WaterBox.y, WaterBox.z  // Simulation volume dimensions (nm)
    
    // Simulation box coordinate ranges:
    -WB.x / 2  to  WB.x / 2
    -WB.y / 2  to  WB.y / 2
    -WB.z / 2  to  WB.z / 2

### **Cell (Subvolume) Properties**
Each **subvolume (cell)** is defined by its size:

.. code-block:: cpp

    subCellSize.x, subCellSize.y, subCellSize.z  // Size of individual cells

- The **total number of divisions** in each dimension is **Nx, Ny, Nz**.

- The **term "subCell"** is used interchangeably with "cell" in the **serial implementation**.

---

Parallel Partitioning Strategy
"""""""""""""""""""""""""""""""

For **N ranks**, the simulation volume is **partitioned along the X-axis**  
into **N contiguous x-bins**.

- Each molecule is assigned to a **cell** within ``SimulVolume.subCellList[]``.

- Cells are grouped into **rank-specific x-bin partitions**.

- The **ranges of each partition** are set in the function:

.. code-block:: cpp

    init_x_domain_and_offset()

These ranges are stored in the **general MPI container** (``mpiContext``):

.. code-block:: cpp

    startCell, endCell       // Rank-specific owned zones
    startGhosted, endGhosted // Ghost zones visible to the rank

A major advantage of **X-direction partitioning** is that **data exchanges**  
between ranks can be efficiently implemented using:

- **Point-to-point nearest neighbor MPI communication**.

---

Looping Over Cells for Data Partitioning
"""""""""""""""""""""""""""""""""""""""""

To prepare **data for parallel execution**, **molecules are grouped into cells**.  
Each **rank** iterates over all cells and applies **partitioning rules**:

1. **Loop over all simulation cells**.
2. **If a cell belongs to the rank's x-bin partition**, process it:
   - **Check if the cell is within the rank’s boundaries** (``startCell`` to ``endCell``).
   
   - **Include ghosted cells** (``startGhosted`` to ``endGhosted``).

3. **Loop over all molecules in the cell’s member list**.
4. **Apply partitioning operations**.

This ensures **efficient data segmentation** for **parallel execution**.

Debugging
~~~~~~~~~

Compared to **serial code**, parallel code is **harder to debug** due to:
- **Concurrent execution** across multiple ranks.

- **Multiple output streams**, making tracking execution more complex.

The **gdb utility** can be used with **mpirun** by starting each **MPI process (rank)**  
with a **separate gdb instance**. This assigns **each rank a separate terminal window**,  
allowing for isolated debugging.

---

Tracking a Single Molecule
"""""""""""""""""""""""""""

Debugging often requires **tracking a single molecule across ranks** during specific iterations.  
To facilitate this, the following were implemented:

1. **The ``debug_print`` function**
2. **Two debugging macros:**
   - ``DEBUG_MOL``
   
   - ``DEBUG_FIND_MOL``

These **macros call ``debug_print``**, as shown below:

.. code-block:: cpp

    #define DEBUG_MOL(s) { debug_print(mpiContext, mol, s); }

    #define DEBUG_FIND_MOL(s) { \
        for(auto &mol : moleculeList) \
            debug_print(mpiContext, mol, s); \
    }

### **How to Use These Macros**
- **``DEBUG_MOL``** → Use inside a function where a molecule is already known.

- **``DEBUG_FIND_MOL``** → Use when searching for a molecule within ``moleculeList``.

The ``debug_print`` function **can be modified** to print additional details of interest.

---

Debugging Functions
"""""""""""""""""""

Several debugging functions, suffixed with **"debug_"**, have been implemented  
to assist in **detecting errors early**. These functions include:

- ``debug_firstEmptyIndex``

- ``debug_bndpartner_interface``

- ``debug_molecule_complex_missmatch``

These functions are **located in** the ``src/debug`` **directory**.

### **Purpose of Debugging Functions**
- Help **identify mismatches** in molecular structures and interactions.

- Ensure **proper indexing** of molecules in parallel execution.

- Assist in **tracing incorrect behavior** in boundary conditions.

---

Best Practices for Debugging Parallel Code
"""""""""""""""""""""""""""""""""""""""""""

When developing the simulator, especially components **affecting parallel execution**,  
programmers are **strongly encouraged** to **use and modify debugging functions**.

### **Detecting Hidden Coding Errors**
Some **errors might not be immediately visible** but can cause **propagation issues**  
in the data structures.  

To mitigate this risk:
- **Before pushing code to the repository**, run **"debug_*" functions** in **each iteration**.

- This ensures that **"impossible-situations" errors** are detected **early**.
