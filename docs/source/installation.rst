Installation Guide
==================

NERDSS
------

NERDSS (NonEquilibrium Reaction-Diffusion Self-assembly Simulator) requires a C++ compiler and the GNU Scientific Library (GSL). Once these prerequisites are installed, you can compile NERDSS from source.

**1. Install a C++ Compiler**
- macOS: Install XCode or Command Line Tools  
- Ubuntu: Install via apt, for example:
  ``sudo apt-get install g++``

**2. Install GNU Scientific Library (GSL) (v2.5+)**
- macOS: Use Homebrew:
  ``brew install gsl``  
- Ubuntu: Use apt:
  ``sudo apt-get install libgsl-dev``

**3. Compile NERDSS**
- Navigate to the main NERDSS directory  
- Run ``make serial``  
- The executable will appear in the ``./bin`` directory

For more details on using NERDSS, see its official documentation or README.

Parallel NERDSS
---------------

To build NERDSS with MPI support, follow these steps:

1. **Install a C++ Compiler with MPI support:**
  - **macOS:** Install OpenMPI with Homebrew:
    ```
    brew install open-mpi
    ```
  - **Ubuntu:** Install OpenMPI through apt:
    ```
    sudo apt install openmpi-bin libopenmpi-dev
    ```

2. **Install GNU Scientific Library (GSL) (v2.5+):**
  - **macOS:** Use Homebrew:
    ```
    brew install gsl
    ```
  - **Ubuntu:** Use apt:
    ```
    sudo apt install libgsl-dev
    ```

3. **Compile NERDSS with MPI support:**
  - Navigate to the main NERDSS directory
  - Run:
    ```
    make mpi
    ```
    (For profiling support, run: `make mpi ENABLE_PROFILING=1`)
  - The executable will appear in the `./bin` directory

### Running Simulations

To start a simulation, use the command:

```bash
mpirun -np 4 ./nerdss_mpi -f parms.inp -s 123
```

ionerdss
--------

``ionerdss`` can be installed directly from PyPI:

.. code-block:: console

   pip install ioNERDSS

After installation, you can import ``ionerdss`` in Python:

.. code-block:: python

   import ionerdss as ion
   ion.some_function()

For tutorials on setting up models and analyzing simulator output, see the :doc:`tutorials`.