Tutorials
=========

The tutorials for **ioNERDSS** are provided as Jupyter notebooks. They demonstrate:

- Setting up models for NERDSS
- Reading/processing simulation outputs
- Generating plots and analyses

Accessing the Notebooks
-----------------------

1. **Local Clone & Jupyter**  
   - Clone the repo (if not already):
     .. code-block:: console

        git clone https://github.com/YourUser/ioNERDSS.git

   - Navigate to the ``tutorial`` folder and launch Jupyter:
     .. code-block:: console

        cd ioNERDSS/tutorial
        jupyter notebook

   - Open each notebook (e.g., ``SingleSpeciesTutorial.ipynb``, ``MultiSpeciesTutorial.ipynb``) to follow along.

2. **Read the Docs**  
   - You can read them here without manually opening Jupyter.

Notebook Index
--------------

.. toctree::
   :maxdepth: 1
   :caption: Jupyter Notebooks

   ioNERDSSTutorialSingle
   ioNERDSSTutorialMulti
   ReadPDBTutorial

Additional Resources
--------------------
- For function-by-function usage, see the :doc:`api_reference`.
- For installation details, see the :doc:`installation`.