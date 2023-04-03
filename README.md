## io_nerdss

This repository primarily contains Python code for creating user-friendly analysis tools for setting up models and analyzing output from the reaction-diffusion simulator NERDSS.

### Branch description

We have created a new development branch where we will be improving the code quality, cleaning up tutorials, optimizing certain functions, and reorganizing directories for better readability.

### Folder Descriptions
**bolded text = sub-directory**

**IoNERDSSPyPi: Holds the main code of the library + extra files necessary for PyPi**
 - **IoNERDSS:** Holds the actual code. Each function can be find as a seperate file in /functions
 - **ioNERDSS.egg-info:** text that is necessary for PyPi

**Tutorial: Holds developer and user tutorials**
 - **DevelopersGuide:** Describes how to edit library, and then upload it to PyPi
 - **MultiSpeciesTutorial:** Desribes how to create graphs and spreadsheets from multi-species assembly NERDSS sim.
    - **Dodecahedron:** NERDSS Multi-Species Input
    - JupyterNotebook: Walks user through how to use different functions required for making graphs and spreadsheets from the NERDSS multi-species output
    - histogram_complexes_time_dode_1 .... _5: NERDSS Multi-Species outputs
    - .png/.csv: IoNERDSS outputted charts and spreadsheets
 - **RealRealPDBTutorial:** Describes how to interpret and edit data from RealPDB NERDSS sim.
    - JupyterNotebook: Walks user through how to use different functions required for interpreting data from RealPDB NERDSS sim & creating new inputs for the NERDSS sim
    - 1si4.pdb (hemoglobin protein) & 1utc.pdb (clathrin protein): NERDSS RealPDB output
    - .mol/.inp: IoNERDSS outputted NERDSS input
    - show_structure.pdb:  IoNERDSS outputted 'simplified' .pdb file for creating graphs of the protein's connections
 - **SingleSpeciesTutorial:** Describes how to use IoNERDSS with NERDSS & how to interpret / edit data from SingleSpecies NERDSS sim.
    - JupyterNotebook: Walks user through how to use different functions required to create inputs for single-species NERDSS sim & for making graphs and spreadsheets from the NERDSS output
    - .mol /parm.inp: IoNERDSS outputted NERDSS inputs
    - histogran_complexes_time_dode_1 ... _5: NERDSS SingleSpecies outputs
    - transition_matrix_time_1 ... _5: NERDSS SingleSpecies outputs
    - restart.dat/9999999.pdb: NERDSS SingleSpecies ouputs
    - output_file: IoNERDSS outputted file. Edited version of restart.dat/9999999.pdb

**ExamplesIoNERDSS: Holds a lot of files that (i may be wrong) seem to be examples of using ioNERDSS.**
 - **LocatePositionByPdbRestart** : an example of using IoNERDSS to interpret data from the pdb / restart / .dat files from the SingleSpecies NERDSS sim
    - **PDB:** Example of using parms.inp + 9999999.pdb to locate positions
    - **restart:** Example of using restart.dat + 9999999.pdb to locate positions
    - Both Include:
        - output_file.pdb: file outputted by the jupyter notebook code
 - **OutputVis:** an example of IoNERDSS using ouputs from Single/MultiSpecies NERDSS sims to create graphs. (code not in a directory is for single species)
     - **multi_components:** same thing but for multispecies
        - **simulation:** seems to be a complete NERDSS output of something
        - **multi_components_sikao:** another example of creating graphs (same data type as before, but new files)
        - JupyterNotebook: shows a lot of examples of creating graphs based on data. Both inports and instantiates (some) functions.
        - histogram_complexes_time ... _5: NERDSS outputs
    - histogran_complexes_time_dode_1 ... _5: NERDSS SingleSpecies outputs
    - transition_matrix_time ... _5: NERDSS SingleSpecies outputs
    - JupyterNotebook: seems to just instantiate all functions that would be necessary, but does not do anything with them. Possibl intended for user to use final box?
    - hist_3d_time.py: python script that generates a graph based on the other files in the folder
    - multi_comp_hist.dat / hist_to_df.csv: unknown
 - **PdbAngleCalculation:** an example of IoNERDSS using ouputs from PDB NERDSS sims to create graphs and new inputs for NERDSS
    - **1utc** : seems to be an example of using IoNERDSS for editing the PDB input. However, the code is seperate from the library, and just .py files here. 
    - **raw_functions:** same as 1utc but only includes the functions
    - 3Dtest.py: unknown
    - JupyterNotebook: instantiates IoNERDSS functions and uses them for various PDB related tasks
    - 1si4/1utc: NERDSS RealPDB output
 - **PlatonicSolids:** examples of creating platonic solids using IoNerds
    - Folders with solid names (ex: Cube, Octahedron)
        - **[name]Face** and **[name]Vertex:** the two files have slightly different contents in each file, but I do not know the difference
            - [name].mole / parm.inp: inputs for NERDSS made by IoNERDSS
            - JupyterNotebook: writes the inputs for NERDSS (instanstiates all functions, does not import)
    - **PyFilesForPlatonicSolids:** includes python files that instantiate functions that can be used to create Platoic Solids that can be inputted in NERDSS. However, the scripts will not create any platonic solids as they only instantiate the functions, maybe intended for user to add their own code at the bottom.
    - **Clath_rotate:** includes 1 JupyterNotebook that instantiates and then runs functions that rotate clathrin (the initial clathrin data is included in the script)



### Install

To install via pip, use the command: 
pip install ioNERDSS

### Syncing PyPi from GitHub

- Navigate to the ioNERDSSPyPi folder
- Ensure that your package's version number in setup.py matches the version number of the PyPI package you want to sync (It should be a newer version). If not, update the version number.
- Create a source distribution of your package by running the following command in your terminal: **python setup.py sdist**. This will create a dist directory containing a tarball of your package's source code.
- Upload the source distribution to PyPI by running the following command: twine upload dist/*

### Best practices

- Use docstrings to document your code. Sphinx can extract docstrings from your code to create documentation, so it's important to write clear and concise docstrings that describe the purpose and functionality of your code.
- Use reStructuredText (reST) markup in your docstrings.
- Follow the Google-style docstring conventions. This is a popular convention for writing docstrings that is widely used in the Python community. It consists of a one-line summary, followed by a more detailed description, and optional sections for parameters, returns, and other details. You can find more information on this convention in the Sphinx documentation.
- Organize your code into modules and packages.
- Use meaningful names for modules, classes, functions, and variables.
- Include examples and usage instructions in documentation. Sphinx can include examples and usage instructions in your documentation, which can help users understand how to use your code.
- Use Sphinx to generate documentation.
- Add tests for each function using unittest.
