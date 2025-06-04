import unittest
import sys
from unittest import mock
import os
import tempfile
import warnings

# Attempt to import Analysis, but allow tests to run even if it fails at module level
# due to other reasons, focusing specific tests on visualize_trajectory.
try:
    from ionerdss.nerdss_analysis.analysis import Analysis
    IONERDSS_ANALYSIS_AVAILABLE = True
except ImportError:
    IONERDSS_ANALYSIS_AVAILABLE = False

# Create a dummy XYZ file content for testing
DUMMY_XYZ_CONTENT = """1
Dummy comment line
Ar 0.0 0.0 0.0
"""

# To simulate missing modules, we can patch sys.modules.
# We need to list all modules that are imported inside the try-except block
# in visualize_trajectory: 'ovito.io', 'ovito.vis', 'imageio', 'PIL.Image'
MISSING_MODULES_CONFIG = {
    'ovito.io': None,
    'ovito.vis': None,
    'imageio': None,
    'PIL.Image': None,
    # 'IPython.display': None # We don't mock IPython.display as it's handled gracefully
}

@unittest.skipIf(not IONERDSS_ANALYSIS_AVAILABLE, "ionerdss.nerdss_analysis.analysis module not available")
class TestAnalysisOptionalDeps(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for saving outputs, if any
        self.temp_dir = tempfile.TemporaryDirectory()
        self.save_folder = self.temp_dir.name # Use a consistent name

        # Ensure the DATA subdirectory exists, mimicking expected structure
        data_dir = os.path.join(self.save_folder, "DATA")
        os.makedirs(data_dir, exist_ok=True)
        
        # Create a dummy trajectory.xyz in the DATA subdirectory
        self.dummy_xyz_file_path = os.path.join(data_dir, "trajectory.xyz")
        with open(self.dummy_xyz_file_path, 'w') as f:
            f.write(DUMMY_XYZ_CONTENT)
            
        # Initialize Analysis instance pointing to the parent of DATA
        self.analysis_instance = Analysis(save_dir=self.save_folder)

    def tearDown(self):
        self.temp_dir.cleanup()
        # No need to explicitly delete self.dummy_xyz_file_path as TemporaryDirectory.cleanup() handles it.

    @mock.patch.dict(sys.modules, MISSING_MODULES_CONFIG) # Removed clear=True from original pytest version
    def test_visualize_trajectory_raises_error_if_deps_missing(self):
        """
        Test that visualize_trajectory raises an ImportError if ovito, imageio, or Pillow are missing.
        """
        with warnings.catch_warnings(): # Suppress OVITO PyPI warning during this test
            warnings.filterwarnings('ignore', message='.*OVITO.*PyPI')
            with self.assertRaises(ImportError) as cm:
                self.analysis_instance.visualize_trajectory(trajectory_path=self.dummy_xyz_file_path)
        
        expected_msg_part_pip = "pip install ionerdss[ovito_rendering]"
        expected_msg_part_conda = "conda install -c conda.ovito.org -c conda-forge ovito imageio pillow"
        self.assertIn(expected_msg_part_pip, str(cm.exception))
        self.assertIn(expected_msg_part_conda, str(cm.exception))

    def test_visualize_trajectory_runs_if_deps_present(self):
        """
        Test that visualize_trajectory runs without raising an ImportError if dependencies are present.
        This test will be skipped if the dependencies are not actually installed.
        """
        try:
            import ovito.io
            import ovito.vis
            import imageio
            from PIL import Image
            # We don't need to check IPython.display for this core functionality test
        except ImportError:
            self.skipTest("Optional dependencies (ovito, imageio, Pillow) not installed. Skipping this test.")

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message='.*OVITO.*PyPI')
            try:
                # We expect this to run. If it raises an error other than ImportError 
                # (which would be caught above if deps are missing), that's a test failure.
                # The function might print to stdout/stderr (e.g. IPython not available) or try to save a file.
                # We are mainly concerned that it doesn't raise an unexpected error due to the dependency handling itself.
                self.analysis_instance.visualize_trajectory(trajectory_path=self.dummy_xyz_file_path, save_gif=False)
            except Exception as e:
                self.fail(f"visualize_trajectory raised an unexpected exception with dependencies present: {e}")

if __name__ == '__main__':
    unittest.main() 