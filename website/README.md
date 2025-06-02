# Website and Documentation (ReadTheDocs)

This folder contains the source files used to build the public-facing documentation website hosted on [Read the Docs](https://readthedocs.org/).

## Structure

```

website/
├── source/             # .rst source files for Sphinx (and images)
│   ├── index.rst
│   ├── guide.rst
│   └── figures/
│       └── diagram.png
├── example.ipynb       # Jupyter notebook shown on the website
├── Makefile            # Standard Sphinx Makefile (Linux/macOS)
├── make.bat            # Windows batch file for Sphinx
├── requirements.txt    # Python dependencies to build the docs
└── conf.py             # Sphinx configuration file

````

## Build Instructions (Locally)

To build the documentation locally for preview:

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
````

2. Build the HTML:

```bash
make html
```

3. Open the output in your browser:

```bash
open _build/html/index.html  # or manually open _build/html/index.html
```

## Modifying Content

* Edit or add `.rst` files inside `source/`.
* Images and figures should go into `source/figures/`.
* To embed a notebook, make sure `nbsphinx` is installed and list the notebook in `index.rst`.

## ReadTheDocs Integration

ReadTheDocs builds the site automatically from this folder using `.readthedocs.yaml` in the root of the repository.

If this folder is renamed (e.g., from `docs/` to `website/`), **you must update** the following line in `.readthedocs.yaml`:

```yaml
sphinx:
  configuration: website/conf.py
```

## Testing Notebook Rendering

To preview notebooks rendered in docs:

* Ensure `nbsphinx`, `ipykernel`, and `jupyter` are in `requirements.txt`
* Run:

```bash
jupyter nbconvert --execute --to html example.ipynb
```

## For Developers

* Only modify this folder if you’re updating the website/docs.
* When adding a new `.rst`, be sure to link it in `source/index.rst` or via `toctree`.
* Test your changes locally with `make html` before pushing.

