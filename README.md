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
import ioNERDSS as ion

# Example usage
ion.nerdss()
```

For extended examples, see the [tutorials](./tutorial/) folder.

---

## Documentation
- **User Guide:** The [.pdf file](./docs/ioNERDSSUserGuide.pdf) in the docs/ folder.

- **API Reference:** Docstrings are integrated throughout the code (Google-style). You can build the docs locally using Sphinx:
```bash
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
├── ioNERDSS/              # Main Python package
│   ├── functions/         # Submodules (e.g., histograms, pdb, etc.)
│   └── __init__.py 
├── tests/                 # Unit tests
├── tutorial/              # Example workflows & tutorials
│   ├── DevelopersGuide/   # For contributors
│   ├── GUITutorial/       # Tutorials for using GUI features
│   ├── MultiSpeciesTutorial/
│   ├── ReadPDBTutorial/   # Updated instructions on PDB usage
│   ├── SingleSpeciesTutorial/
│   └── ...                # Additional tutorials
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