.. ionerdss documentation master file, created by
   sphinx-quickstart on Thu Jun 13 12:16:26 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ionerdss Documentation!
==================================

**NERDSS** (NonEquilibrium Reaction-Diffusion Self-assembly Simulator) is a simulator for reaction-diffusion processes.
**ionerdss** is a Python package that streamlines setting up models and analyzing output from NERDSS. Input files can be generated from structures of macromolecular complexes, such as those defined in Protein Data Bank (PDB) files or based on the idealized geometries of Platonic solids. The package is designed to improve the usability and quantitative interpretation of NERDSS simulations.

Features of ionerdss:

- **Creating NERDSS Inputs:** Automatically creates executable NERDSS inputs for you.
   - **Protein Data Bank (PDB) files:** Generates NERDSS input files from PDB files.
   - **Platonic solids:** Generates NERDSS input files from idealized geometries of Platonic solids, with 2 options for each of the 5 Platonic solids.

This documentation includes:

- How to install and compile NERDSS
- NERDSS and ionerdss documentation  
- How to install ionerdss  
- ionerdss Tutorials (via Jupyter notebooks)  
- Release notes for both NERDSS and ioNERDSS  
- An auto-generated API reference for `ionerdss`

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   installation
   downloads
   release_notes
   nerdss_documentation
   ionerdss_documentation
   ionerdss_tutorials
   api_reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
