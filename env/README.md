
# Environment Setup

This folder contains configuration files for setting up the Python environment required for this project.

## Options

You can set up the environment using either **Conda** or **pip**, depending on your preference.

---

## Option 1: Using Conda (`environment.yml`)

This is the recommended method if you have Conda (via [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)) installed.

```bash
# From the project root
conda env create -f env/environment.yml
conda activate ionerdss_env
````

To update the environment later if the file changes:

```bash
conda env update -f env/environment.yml --prune
```

---

## Option 2: Using pip (`requirements.txt`)

This method is useful if you prefer a lightweight virtual environment without Conda.

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate     # On Windows use: .venv\Scripts\activate

# Install requirements
pip install -r env/requirements.txt
```

---

## Files in this folder

* `environment.yml` — full Conda environment specification (Python version, dependencies, pip fallback).
* `requirements.txt` — pip-compatible list of required packages.

---

## Notes

* Be sure to activate your environment before running any scripts or launching notebooks.
* Jupyter users: the Conda environment includes `ipykernel` so you can run notebooks under this environment.

```bash
python -m ipykernel install --user --name ionerdss_env --display-name "Python (ionerdss_env)"
```

---

## Questions

If you're unsure which setup to use, start with **Conda** if available.
