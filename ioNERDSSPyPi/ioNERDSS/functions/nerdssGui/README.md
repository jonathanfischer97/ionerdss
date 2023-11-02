# Install lib

```bash
conda create --name myenv python=3.9
conda activate myenv
conda install pip
pip install numpy, pandas, matplotlib, seaborn, tqdm, PyQt6, pyqtgraph, PyOpenGL, biopython
pip install pyqt6-tools
```

```bash
python main.py
```

# For developer

generate the .ui file using `designer`

convert the .ui to gui.py:
```bash
pyuic6 -x path_to_ui.ui -o gui.py
```
