## io_nerdss
This repository primarily contains Python code for creating user-friendly analysis tools for setting up models and analyzing output from the reaction-diffusion simulator NERDSS.

### Branch description
We have created a new development branch where we will be improving the code quality, cleaning up tutorials, optimizing certain functions, and reorganizing directories for better readability.

### Install
To install via pip, use the command: 
pip install ioNERDSS

### Syncing PyPi from GitHub
- Navigate to the ioNERDSSPyPi folder
- Ensure that your package's version number in setup.py matches the version number of the PyPI package you want to sync. If not, update the version number.
- Create a source distribution of your package by running the following command in your terminal: **python setup.py sdist**. This will create a dist directory containing a tarball of your package's source code.
- Upload the source distribution to PyPI by running the following command: twine upload dist/*
