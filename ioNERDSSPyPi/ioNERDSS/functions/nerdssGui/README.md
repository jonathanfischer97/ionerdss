# Install lib

```bash
conda create --name myenv python=3.9
conda activate myenv
conda install pyqt
conda install -c conda-forge pyqtgraph
conda install pyopengl
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda install biopython
```

```bash
python main.py
```

# For developer

generate the .ui file using `designer`

convert the .ui to gui.py:
```bash
pyuic5 -x path_to_ui.ui -o gui.py
```
