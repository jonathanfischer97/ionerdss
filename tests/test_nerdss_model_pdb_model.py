import unittest
import json
import math
import tempfile
from pathlib import Path

from ionerdss import PDBModel

def is_number(val):
    try:
        float(val)
        return True
    except (TypeError, ValueError):
        return False

def compare_values(val1, val2, tol=0.01, path="root"):
    if isinstance(val1, dict) and isinstance(val2, dict):
        if set(val1.keys()) != set(val2.keys()):
            print(f"Key mismatch at {path}: {val1.keys()} != {val2.keys()}")
            return False
        return all(
            compare_values(val1[k], val2[k], tol, f"{path}.{k}") for k in val1
        )

    elif isinstance(val1, list) and isinstance(val2, list):
        if len(val1) != len(val2):
            print(f"List length mismatch at {path}: {len(val1)} != {len(val2)}")
            return False
        return all(
            compare_values(v1, v2, tol, f"{path}[{i}]")
            for i, (v1, v2) in enumerate(zip(val1, val2))
        )

    elif is_number(val1) and is_number(val2):
        f1, f2 = float(val1), float(val2)
        if not math.isclose(f1, f2, abs_tol=tol):
            print(f"Value mismatch at {path}: {f1} != {f2} (tol={tol})")
            return False
        return True

    else:
        if val1 != val2:
            print(f"Exact mismatch at {path}: {val1} != {val2}")
            return False
        return True

class TestPDBModelOutput(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.save_folder = Path(self.temp_dir.name)
        self.pdb_id = '8y7s'
        self.expected_path = Path("data/8y7s_model.json")
        self.actual_path = self.save_folder / f"{self.pdb_id}_model.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_model_output_against_expected(self):
        pdb_model = PDBModel(pdb_id=self.pdb_id, save_dir=str(self.save_folder))

        pdb_model.coarse_grain(
            distance_cutoff=0.35,
            residue_cutoff=3,
            show_coarse_grained_structure=False,
            save_pymol_script=False,
            standard_output=False
        )

        pdb_model.regularize_homologous_chains(
            dist_threshold_intra=3.5,
            dist_threshold_inter=3.5,
            angle_threshold=25.0,
            show_coarse_grained_structure=False,
            save_pymol_script=False,
            standard_output=False
        )

        with open(self.expected_path, "r") as f_expected:
            expected_data = json.load(f_expected)

        with open(self.actual_path, "r") as f_actual:
            actual_data = json.load(f_actual)

        self.assertTrue(
            compare_values(expected_data, actual_data, tol=0.01),
            "The actual model output does not match the expected output within the tolerance."
        )


if __name__ == "__main__":
    unittest.main()
