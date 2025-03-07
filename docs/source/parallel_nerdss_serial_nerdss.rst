Serial NERDSS
~~~~~~~~~~~~~

Serial NERDSS is a particle and rigid-body structure-resolved reaction-diffusion software. In this system, the molecule is the fundamental simulation object. Each molecule is characterized by a center-of-mass and one or more interfaces capable of binding to a single interface from another molecule. Multiple molecules can form a Complex via interface binding, and a single molecule is also assigned to a Complex of size 1. Both intramolecular and intracomplex flexibility are not allowed; all species are rigid bodies.

Simulation Environment
^^^^^^^^^^^^^^^^^^^^^^

1. A vector of molecules stores all molecules present in the system.
2. Each molecule is assigned a unique index property, corresponding to its position within the vector.
3. Each molecule contains a vector of interfaces.
4. Each interface is assigned an index property, representing its position within the molecule’s interfaces vector.
5. Each interface can have more than one state and can change its state during the simulation.
6. A vector of complexes stores all complexes formed in the system.
7. Each complex is assigned a unique index property, corresponding to its position within the vector.
8. Each complex has a vector of integers named `memberList`, storing all indexes of molecules forming this complex.
9. Each molecule has a `myComIndex` property storing the index of the complex to which it belongs.

This organizational structure allows for efficient tracking of molecular interactions and complex formations. An interface can identify its binding partner (both the molecule and the specific interface) by storing the corresponding indexes.

Sub-volume Optimization
^^^^^^^^^^^^^^^^^^^^^^^

To enhance computational efficiency, we implemented a sub-volume division strategy in the serial code. Each sub-volume only evaluates interactions within itself and with adjacent sub-volumes. In 3D, each sub-volume has 26 neighboring sub-volumes (ignoring boundaries).

1. **Cutoff Distance**: We calculate a cutoff distance based on the largest separation between species that can still result in a bimolecular reaction. Beyond this distance, molecules are too far apart to collide and interact with one another.
2. **Spatial Division**: The simulation volume is partitioned into sub-volumes, each with dimensions greater than or equal to the cutoff distance. This division guarantees that binding interactions between interfaces can only occur within the same sub-volume or between adjacent sub-volumes. This significantly reduces the number of interface pairs that need to be checked for potential reactions.
3. **Balance Consideration**: While increasing the number of sub-volumes improves efficiency, an excessive number will slow down the simulation due to the computational overhead of iterating through all sub-volumes and their adjacent neighbors. To maintain optimal performance in the serial version of the simulator, we do not allow more sub-volumes than there are particles.

Pseudo code for Serial NERDSS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following pseudo code outlines the reaction-diffusion process in the Serial
version of the simulator. Key constraints include:

- Each molecule can participate in only one reaction per iteration step, even if it has multiple interfaces.

- If a molecule does not react, it moves as a rigid body.

- If a complex has multiple molecules, each molecule is allowed to attempt a reaction independently.

- If a complex does not react, it diffuses as a rigid body during that iteration step.

- Steric overlaps are prevented.

Reaction-Diffusion Simulation (Serial Version)

// Initialization

1. Generate all molecules and corresponding complexes

    - Store molecules in vector: `moleculeList`
    
    - Store complexes in vector: `complexList`

2. Calculate the `cutoff_distance`

    - Divide simulation volume into sub-volumes based on `cutoff_distance`
    
    - Store sub-volumes in vector: `subVolList`
    
    - For each `subVol` in `subVolList`:
      
      - Initialize vector<int> `memberMolList`
    
    - For each molecule in `moleculeList`:
      
      - Set `molecule.mySubVolIndex` to appropriate subVol index

// Main Simulation Loop

3. For `iteration = 1` to `max_iterations`:

    4. Update subVol memberships:

        - For each `subVol` in `subVolList`:
          
          - Clear `subVol.memberMolList`
        
        - For each molecule in `moleculeList`:
          
          - Update `molecule.mySubVolIndex`
          
          - Append `molecule.index` to `subVol.memberMolList`
    
    5. Process zeroth-order and first-order reactions:

        - Check and perform:
          
          - Molecule creation
          
          - Molecule destruction
          
          - Unimolecular state changes
          
          - Complex dissociation
    
    6. Calculate and store binding probabilities for all possible second-order bimolecular reactions:

        If the molecule interface already participated in a 0th or 1st order reaction, it can only have binding probabilities set to zero. This applies to all interfaces on the molecule. They must still be evaluated for second-order reactions, so that they will avoid overlap with reaction partners that are close by. The other elements of the complex (if the molecule is part of a complex) are not restricted from reacting, but are restricted from diffusing.
        
        - For each `subVol` in `subVolList`:
          
          - For each `molecule1` in `subVol.memberMolList`:
             
             - For each `molecule2` in `subVol.memberMolList`:
                
                - If `binding_possible(molecule1, molecule2)`:
                  
                  - Store binding information in `molecule1` and `molecule2`
             
             - For each `subVol` in `adjacentSubVols`:
                
                - For each `molecule2` in `subVol.memberMolList`:
                  
                  - If `binding_possible(molecule1, molecule2)`:
                     
                     - Store binding information in `molecule1` and `molecule2`
    
    7. Perform second-order bimolecular reactions:

        - For each molecule in `moleculeList`:
          
          - Compare the binding probabilities to a URN. If the probability is > URN, perform the reaction.
          
          - Perform bimolecular reactions by associating molecule pair into their defined ‘bound’ orientation.
    
    8. Perform diffusion for unreacted complexes:

        - For each molecule in `moleculeList`:
          
          - If molecule has not undergone a 0th, 1st, or 2nd order reaction, or is not part of a complex that has undergone one of these reactions:
             
             - Diffuse its complex as a rigid body
             
             - Ensure no steric overlaps occur with all molecules in its partner list, including molecules that have undergone reactions.
    
    9. Reset reaction information:

        - For each molecule in `moleculeList`:
          
          - Clear reaction status and information
    
    10. Update simulation time and collect data as needed

// End of main simulation loop

Data Structures of NERDSS
^^^^^^^^^^^^^^^^^^^^^^^^^

3.1 Coord
    - Stores 3-D coordinates (x, y, z) as doubles.

3.2 SimulVolume
    - Contains simulation volume information.

    - SubVolume structure includes:

        - xIndex, yIndex, zIndex: cell dimensional indices.
        
        - absIndex: flattened dimensional index (xIndex + yIndex * Nx + zIndex * Nx * Ny).
        
        - memberMolList: list of molecule indices within a cell.
        
        - neighborList: list of neighbor cell indices.
    
    - subCellList: vector of SubVolume structures.
    
    - Dimensions structure includes:
        
        - x, y, z: number of cells in each direction.
        
        - tot: total number of sub-volumes.

3.3 MolTemplate
    - Contains properties of each molecule type.
    
    - molTypeIndex: references molecule type.
    
    - interfaceList: list of Interface structures for binding.
    
    - monomerList: lists molecule indices for monomers.

3.4 Reactions
    - Defines possible reactions:
        
        - Bimolecular (association/dissociation).
        
        - BiMolStateChange (X(state1) + Y -> X(state2) + Y).
        
        - UniMolStateChange (X <-> X*).
        
        - ZerothOrderCreation (0 -> X).
        
        - Destruction (destroys entire molecule/complex).
        
        - UniMolCreation (X -> X + Y).

3.5 Molecule
    - Main structure containing molecule and interface information.
    
    - Fields include:
        
        - index: position in moleculeList.
        
        - partnerIndex: bound partner index.
        
        - partnerIfaceIndex: interface index of the partner.
        
        - comCoord: center of mass coordinate.
        
        - isEmpty: true if the molecule is destroyed.
        
        - numberOfMolecules: static counter for molecules.
        
        - emptyMolList: list of indices to empty molecules.
    
    - interfaceList: vector of Iface structures.
    
    - Interaction structure in Iface includes:
        
        - partnerIndex: bound partner molecule index.
        
        - partnerIfaceIndex: interface index of the partner.
        
        - conjBackRxn: back reaction for the interaction.

3.6 Complex
    - Initially, each molecule is a complex. Hence, initially every molecule has its own Complex structure (coincidentally and initially the index for the molecule and complex are the same). Just like moleculeList, a list of all Complex (structures) is maintained in main as vector<Complex> complexList. The myComIndex variable in the molecule structure is the index (position) in complexList of its associated complex. This index is also stored in an Index variable of the Complex structure. When a bond forms, one of the complex structures of the molecule becomes the complex (the other complex is marked isEmpty).
    
    - Fields include:
        
        - index: position in complexList.
        
        - memberList: list of member molecule indices.
        
        - isEmpty: true if the complex is void.
        
        - numberOfComplexes: static counter for complexes.
        
        - comCoord: center of mass coordinate.
