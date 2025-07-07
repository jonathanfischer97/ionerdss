import sys
from pathlib import Path
# Ensure src directory is on sys.path for tests
src_path = Path(__file__).resolve().parents[1] / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
