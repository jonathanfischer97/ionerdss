# ionerdss
[![Documentation Status](https://readthedocs.org/projects/ionerdss/badge/?version=latest)](https://ionerdss.readthedocs.io/en/latest/?badge=latest)
[![Run Unit Tests](https://github.com/JohnsonBiophysicsLab/ionerdss/actions/workflows/unittest.yml/badge.svg?branch=main&event=push)](https://github.com/JohnsonBiophysicsLab/ionerdss/actions/workflows/unittest.yml)
![PyPI](https://img.shields.io/pypi/v/ioNERDSS.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ioNERDSS.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/ioNERDSS.svg)

**ionerdss** is a Python library that provides user‐friendly tools for setting up and analyzing output from the [NERDSS](https://github.com/JohnsonBiophysicsLab/NERDSS) reaction‐diffusion simulator. Its goal is to streamline model building (from PDB files or from scratch), data analysis, and visualization for simulation workflows.

---

## Installation

Install the latest release directly from PyPI:

```bash
pip install ioNERDSS
```

To install from source (e.g., if you’ve cloned this repo and want the most recent changes):

```bash
git clone https://github.com/JohnsonBiophysicsLab/ionerdss.git
cd ionerdss
python setup.py install
```

---

## Quick Start

```python
import ionerdss as ion

# Example usage
ion.nerdss()
```

For extended examples, see the [tutorials](https://ionerdss.readthedocs.io/en/latest/ionerdss_tutorials.html).

---

## Documentation
- **User Guide:** [ionerdss user guide](https://ionerdss.readthedocs.io/en/latest/ionerdss_documentation.html).

- **API Reference:** [API](https://ionerdss.readthedocs.io/en/latest/ionerdss.html) .Docstrings are integrated throughout the code (Google-style). You can also build the docs locally using Sphinx:
```bash
sphinx-apidoc -o docs/source ionerdss
cd docs
make html
```
Then open docs/build/html/index.html in your browser.

---

## Repository Structure
```
ionerdss/
├── .github/workflows/     # Continuous Integration workflows
├── docs/                  # Documentation (Sphinx configs, user guides)
│   ├── source/            # Sphinx source files
│   ├── make.bat           # Windows build script
│   └── Makefile           # Unix build script
├── ionerdss/              # Main Python package
│   ├── model_setup/       # Model building tools
│   ├── analysis/          # Data analysis tools
│   └── __init__.py 
├── tests/                 # Unit tests, to be added
├── data/                  # Test and tutorial data
└── setup.py               # Installation & packaging
```

---

## Develop using docker container:  
```bash
docker build --no-cache -t ionerdss_dev . 
docker run -it --rm -v $(pwd):/app -p 8888:8888 ionerdss_dev
```

---

## Best Practices

1. **Docstrings & Sphinx**  
   - Write clear docstrings in Google‐style to help auto‐generate documentation.

   Prompt used for chatGPT to refactor one function: `improve this python code, provide the detail google-style docstring for sphinx, standardize naming conventions:`

2. **Code Organization**  
   - Keep related functionality grouped in submodules.

3. **Tests**  
   - Add or update unit tests in `tests/` for any new function. We use [unittest](https://docs.python.org/3/library/unittest.html).

   - To run the tests locally, in the project root folder, use the following command:
     ```bash
     pip install -r requirements.txt
     export PYTHONPATH=$(pwd)
     pytest
     ```

4. **Versioning & Releases**  
   - Update `setup.py` with a new version number. A GitHub release will auto‐update the PyPI package.

5. **Contributions**  
   - Fork the repo, create a feature branch, and open a pull request.

---

## License
This project is licensed under the GPL‐3.0 License.

## Run a quick trial with Google Colab

Click the following link to make a copy of the iPython notebook in your Google Colab and following the instructions on the Notebook to run a quick trial of the NERDSS simulator with the usage of ionerdss to prepare the inputs from a PDB structure.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JohnsonBiophysicsLab/ionerdss/blob/main/docs/Run_NERDSS_colab.ipynb?copy=true)
