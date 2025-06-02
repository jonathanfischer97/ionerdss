Release Notes
=============

Below is a summary of recent changes for both **NERDSS** and **ionerdss**. For more detailed commit history, please see the respective GitHub repositories.

NERDSS
------

- **New Website**

  A dedicated NERDSS site is now live at  
  https://mjohn218.github.io/NERDSS/

- **NERDSS v1.2.1 (Mar 22, 2025)**

  This release addresses the loop closure issue that occurs when reaction rates are high.

- **Parallel NERDSS v1.0.0 (Dec 2024)**

  A parallelized version of NERDSS is available to speed up simulations on multiple processors.  
  For more information, visit the `NERDSS MPI branch on GitHub <https://github.com/mjohn218/NERDSS/tree/mpi>`_.

ionerdss
--------

- **Version 1.1.0 (Mar 22, 2025)**  

  - Refactored the code into `nerdss_model`, `nerdss_simulation`, and `nerdss_analysis` modules.

  - Unified figure plotting with the `plot_figure()` function in the `analysis` class.

  - Added the ability to visualize model structure compared with PDB structure in Jupyter Notebooks using PyMOL.

  - Added the ability to visualize trajectories in Jupyter Notebooks using OVITO.

  - The previous unrefactored functions are retained in the `analysis` and `model_setup` modules for backward compatibility.
  
- **Version 1.0.37 (Mar 7, 2025)**  

  - This release introduces a new feature to regularize homo chains in PDB structures to the same NERDSS molecule type.

- **Version 1.0.36 (Jan 23, 2025)**  

  - The repository has been moved to the [JohnsonBiophysicsLab organization](https://github.com/JohnsonBiophysicsLab).
