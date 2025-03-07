Running a Restart Simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

During a normal run of NERDSS, a special file called `restart.dat` is written at intervals specified by the user (see `.inp` file parameters section). A restart simulation allows you to start a new simulation from a timestep in a previous simulation at which a restart file was written. `.inp` and `.mol` files are not required for a restart simulation.

To restart a simulation successfully, ensure the following files are in the same directory as the executable:
- Restart file (by default `restart.dat`)

- Trajectory file (optional): A new trajectory file will be created if not provided. If restarting the simulation from a checkpoint, modify the input trajectory file to make it consistent with the restart timepoint, or restart the simulation without the input trajectory file and concatenate all the trajectory files after the simulation.

- `rng_state` file (optional): To restart using the exact same sequence of random numbers, you will need the `rng_state` file. These are only created if the parameter `debugRNG` is set to `true` in the main executable `nerdss.cpp`. By default, `debugRNG` is `false`.

Run the restart simulation with the following command:

.. code-block:: bash

  ./nerdss -r <restart_file>

Where `<restart_file>` is the restart file.

Restarting and Modifying the System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When restarting, it can be beneficial to adapt the system by changing the parameters or by adding molecules and/or reactions. This can be done by also reading in a `.inp` file that is formatted the same way as the `parms.inp` file. This new parameter file can be used to add additional species, change/overwrite the simulation parameters within the parameter block, and to add additional reactions. It cannot be used to modify the rates in existing reactions—that must be modified by changing the values stored in the `restart.dat` file.

Run the restart simulation with modifications using the following command:

.. code-block:: bash

  ./nerdss -r <restart_file> -a <add_parameters_file>

Where `<restart_file>` is the restart file and `<add_parameters_file>` is the parameter file containing new parameters/species/reactions.