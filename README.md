## io_nerdss
This repository primarily contains Python code for creating user-friendly analysis tools for setting up models and analyzing output from the reaction-diffusion simulator NERDSS.

### Branch description
We have created a new development branch where we will be improving the code quality, cleaning up tutorials, optimizing certain functions, and reorganizing directories for better readability.

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
