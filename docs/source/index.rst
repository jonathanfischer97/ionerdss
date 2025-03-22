.. ionerdss documentation master file, created by
   sphinx-quickstart on Thu Jun 13 12:16:26 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ionerdss Documentation!
==================================

**NERDSS** (NonEquilibrium Reaction-Diffusion Self-assembly Simulator) is a simulator for reaction-diffusion processes.
**ionerdss** is a Python package that streamlines setting up models, run NERDSS simulations, and analyzing output from NERDSS. Input files can be generated from structures of macromolecular complexes, such as those defined in Protein Data Bank (PDB) files. ionerdss is designed to improve the usability and quantitative interpretation of NERDSS simulations.

Features of ionerdss:

- **Creating NERDSS Inputs:** Automatically generates executable NERDSS input files.
   - **Protein Data Bank (PDB) files:** Converts PDB files into NERDSS input files. See the `PDB to NERDSS tutorial <pdb_to_nerdss_tutorial.html>`_ for more details.
   - **Platonic solids:** Creates NERDSS input files from idealized geometries of Platonic solids, offering two options for each of the five Platonic solids. See the `Platonic solids tutorial <model_setup_for_platonic_solid.html>`_ for more details.
   - **User designed molecules and reactions**: `JAVA GUI <java_gui_tutorial.html>`_ or `Python GUI <ionerdss_gui.html>`_ allow users to define their own molecules and reactions.

- **Running NERDSS Simulations:** Install NERDSS, modify simulation parameters, and run simulations.
   - See the `PDB to NERDSS tutorial <pdb_to_nerdss_tutorial.html>`_ for more details.

- **Analyzing NERDSS Outputs:** Produces graphs, and visulaizes trajectories from NERDSS outputs.
   - **Histogram Analysis:** Processes and outputs data from histogram.dat files.
   - **Complex Location Analysis:** Determines the location of specific complex sizes using PDB, restart, or input files.
   - **Transition Matrix Analysis:** Reads transition matrix files and generates various outputs.
   - **XYZ File Analysis:** Processes .xyz files, which report coordinates for specific timestamps, and generates various outputs.


This documentation includes:

- How to install NERDSS and ionerdss
- Release notes for both NERDSS and ioNERDSS  
- NERDSS and ionerdss documentation (user guides and developer guides)
- ionerdss Tutorials (via Jupyter notebooks)  
- An auto-generated API reference for `ionerdss`

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   release_notes
   nerdss_documentation
   ionerdss_documentation_v1_1
   ionerdss_documentation_v1_0
   ionerdss_tutorials
   api_reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
