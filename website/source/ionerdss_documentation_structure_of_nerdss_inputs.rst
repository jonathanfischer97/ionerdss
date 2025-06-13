Structure of the NERDSS Input Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NERDSS requires two input files to simulate a model: a parameter file (`parms.inp`) and a molecule structure file for each species in the system (`SPECIES1.mol`, `SPECIES2.mol`, etc.).

**INP Files:** The main input file for NERDSS that includes simulation parameters.

- **Includes:** timesteps, dimensions, included molecules, and reactions.

**MOL Files:** Each file stores information about each included molecule.

- **Includes:** name, diffusion constants, Center of Mass,  binding sites.

For more information, refer to the `NERDSS User Guide <nerdss_user_guide_input_output.html>`_.