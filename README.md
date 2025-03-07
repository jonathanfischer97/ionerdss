# ionerdss
[![Documentation Status](https://readthedocs.org/projects/ionerdss/badge/?version=latest)](https://ionerdss.readthedocs.io/en/latest/?badge=latest)

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

For extended examples, see the [tutorials](./tutorial/) folder.

---

## Documentation
- **User Guide:** The [.pdf file](./docs/ioNERDSSUserGuide.pdf) in the docs/ folder.

- **API Reference:** Docstrings are integrated throughout the code (Google-style). You can build the docs locally using Sphinx:
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
└── setup.py               # Installation & packaging
```

---

## Best Practices

1. **Docstrings & Sphinx**  
   - Write clear docstrings in Google‐style to help auto‐generate documentation.

2. **Code Organization**  
   - Keep related functionality grouped in submodules.

3. **Tests**  
   - Add or update unit tests in `tests/` for any new function. We use [unittest](https://docs.python.org/3/library/unittest.html).

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
