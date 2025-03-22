Installation Guide
==================

NERDSS
------

NERDSS (NonEquilibrium Reaction-Diffusion Self-assembly Simulator) requires a C++ compiler and the GNU Scientific Library (GSL). Once these prerequisites are installed, you can compile NERDSS from source.

**0. Download the NERDSS source code from the official repository**

.. code-block:: console

   git clone https://github.com/mjohn218/NERDSS.git
   cd NERDSS

**1. Install a C++ Compiler**

- macOS: Install XCode or Command Line Tools  

- Ubuntu: Install via apt, for example:

.. code-block:: console

   sudo apt-get install g++

**2. Install GNU Scientific Library (GSL) (v2.5+)**

- macOS: Use Homebrew:

.. code-block:: console

   brew install gsl  

- Ubuntu: Use apt:

.. code-block:: console

   sudo apt-get install libgsl-dev

**3. Compile NERDSS**

- Run 

.. code-block:: console

   make clean
   make serial 

- The executable `nerdss` will appear in the `./bin` directory

For more details on using NERDSS, see its `documentation <nerdss_documentation.html>`_.

Parallel NERDSS
---------------

To build NERDSS with MPI support, follow these steps:

**1. Install a C++ Compiler with MPI support:**

- **macOS:** Install OpenMPI with Homebrew:

.. code-block:: console

   brew install open-mpi

- **Ubuntu:** Install OpenMPI through apt:

.. code-block:: console

   sudo apt install openmpi-bin libopenmpi-dev

**2. Install GNU Scientific Library (GSL) (v2.5+):**

- **macOS:** Use Homebrew:

.. code-block:: console

   brew install gsl

- **Ubuntu:** Use apt:

.. code-block:: console

   sudo apt install libgsl-dev

**3. Compile NERDSS with MPI support:**

- Checkout to the `mpi` branch:

.. code-block:: console

   git checkout mpi

- Run:

.. code-block:: console

   make clean
   make mpi

- The executable `nerdss_mpi` will appear in the `./bin` directory

**4. Running Simulations**

To start a parallel simulation, use the command:

.. code-block:: console

   mpirun -np 4 ./nerdss_mpi -f parms.inp

ionerdss
--------

`ionerdss` can be installed directly from PyPI (recommend to conda environment):

**0. Create a conda environment (optional but recommended)**

Download and install Anaconda or Miniconda, then create a new conda environment for `ionerdss`:

.. code-block:: console

   conda create -n ionerdss python=3.9
   conda activate ionerdss

**1. Install ioNERDSS**

.. code-block:: console

   pip install ioNERDSS

After installation, you can import `ionerdss` in Python or Jupyter Notebook:

.. code-block:: python

   import ionerdss as ion
   ion.some_function()

For documentation on setting up models and analyzing simulator output, see the `ionerdss tutorial <pdb_to_nerdss_tutorial.html>`_.
