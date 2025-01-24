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

ioNERDSS
--------

``ioNERDSS`` can be installed directly from PyPI:

.. code-block:: console

   pip install ioNERDSS

After installation, you can import ``ioNERDSS`` in Python:

.. code-block:: python

   import ioNERDSS as ion
   ion.some_function()

For tutorials on setting up models and analyzing simulator output, see the :doc:`tutorials`.