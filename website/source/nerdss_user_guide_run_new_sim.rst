Starting a Simulation With NERDSS
---------------------------------

To start a new simulation, you need a parameter file with a `.inp` extension and all the required `.mol` files. The `.mol` files specify the structure of specific molecules, including the location of all interfaces, as well as translational and rotational diffusion constants. The `.inp` files control reaction rules and simulation settings. All input files can be automatically generated using the `ionerdss` package or the provided JAVA GUI.

Once you have all the necessary input files correctly formatted, you can run NERDSS using the following command:

.. code-block:: bash

    ./nerdss -f <your_param_file>

Ensure that all required `.mol` files referenced by the parameter file are in the same directory as the executable.

Here are some useful flags you can use with the `nerdss` command:

.. list-table::
   :header-rows: 1

   * - Flag
     - Description
   * - ``-f <filename>``, ``--parmfile <filename>``
     - Specifies the parameter file (required).
   * - ``-s <integer>``, ``--seed <integer>``
     - Manually sets a seed for the random number generator (optional).
   * - ``-r <filename>``, ``--restart <filename>``
     - Specifies the restart file (required for restart simulation).
   * - ``-a <filename>``, ``--add <filename>``
     - During a restart, reads updated and new parameters, adding to or overriding those in the original parameter file (optional).
   * - ``--debug-force-dissoc``
     - Forces dissociation to occur whenever possible (optional, for debugging only).
   * - ``--debug-force-assoc``
     - Forces association to occur whenever possible (optional, for debugging only).
     