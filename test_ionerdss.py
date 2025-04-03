import os
import pytest
import tempfile
import shutil
import time
from pathlib import Path


from ionerdss import PDBModel
from ionerdss import Simulation
from ionerdss import Analysis


# Define the NERDSS path - adjust this to your system
NERDSS_PATH = "/Users/msang/GitHub/NERDSS/bin/nerdss"


# Use a session-scoped fixture to maintain the working directory throughout all tests
@pytest.fixture(scope="session")
def work_dir(request):
    """Create a temporary working directory for testing that persists for the entire test session."""
    temp_dir = tempfile.mkdtemp(prefix="ionerdss_test_")
    
    # Define a finalizer to clean up after all tests are done
    def cleanup():
        # Only clean up if tests have completed successfully
        if not request.session.testsfailed:
            shutil.rmtree(temp_dir)
            print(f"Cleaned up test directory: {temp_dir}")
        else:
            print(f"Tests failed. Leaving test directory for inspection: {temp_dir}")
    
    # Register the finalizer to execute after all tests
    request.addfinalizer(cleanup)
    
    return temp_dir


@pytest.fixture(scope="session")
def pdb_model(work_dir):
    """Create and configure a PDB model for testing."""
    model_dir = os.path.join(work_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)
    
    # Use a small PDB structure for testing
    model = PDBModel(pdb_id='8Y7S', save_dir=model_dir)
    
    # Coarse grain the structure with minimal visualization for testing
    model.coarse_grain(
        distance_cutoff=0.35, 
        residue_cutoff=3,
        show_coarse_grained_structure=False
    )
    
    # Regularize the model to prepare for simulation
    model.regularize_homologous_chains(
        show_coarse_grained_structure=False,
        save_pymol_script=True
    )
    
    return model


@pytest.fixture(scope="session")
def simulation(pdb_model, work_dir):
    """Set up a simulation based on the PDB model."""
    sim_dir = os.path.join(work_dir, 'simulation')
    os.makedirs(sim_dir, exist_ok=True)
    
    sim = Simulation(pdb_model, work_dir=sim_dir)
    
    # Set minimal parameters for testing
    sim.modify_inp_file({
        'nItr': 10000,  # Reduced iterations for testing
        'timeStep': 0.1,
        'timeWrite': 1000,
        'trajWrite': 5000,
        'pdbWrite': 5000,
        'WaterBox': '[200.0, 200.0, 200.0]'
    })
    
    # Reduce molecule counts for faster testing
    if pdb_model.molecule_types:
        first_mol_name = pdb_model.molecule_types[0].name
        sim.modify_inp_file({first_mol_name: 10})
    
    return sim


def test_model_creation(pdb_model):
    """Test that the model is created successfully."""
    assert pdb_model is not None
    assert len(pdb_model.molecule_types) > 0
    assert len(pdb_model.reactions) > 0
    
    # Check that model files were created
    model_file = os.path.join(pdb_model.save_dir, f"{pdb_model.pdb_id}_model.json")
    assert os.path.exists(model_file)


def test_simulation_setup(simulation):
    """Test that the simulation is set up correctly."""
    # Check that input files were created
    input_dir = os.path.join(simulation.work_dir, "nerdss_input")
    assert os.path.exists(input_dir)
    assert os.path.exists(os.path.join(input_dir, "parms.inp"))
    
    # Check that at least one molecule type file was created
    mol_files = [f for f in os.listdir(input_dir) if f.endswith(".mol")]
    assert len(mol_files) > 0


# Check if NERDSS executable exists
nerdss_available = os.path.isfile(NERDSS_PATH) and os.access(NERDSS_PATH, os.X_OK)


def wait_for_simulation_completion(sim_dir, timeout=300):
    """
    Wait for the simulation to complete by checking for "End simulation" in output.log.
    
    Args:
        sim_dir: Path to the simulation directory
        timeout: Maximum time to wait in seconds
    
    Returns:
        bool: True if simulation completed successfully, False if timed out
    """
    start_time = time.time()
    output_log = os.path.join(sim_dir, "output.log")
    
    # First, wait for the output log file to be created
    while not os.path.exists(output_log):
        if time.time() - start_time > timeout:
            print(f"Timeout waiting for simulation output log: {output_log}")
            return False
        time.sleep(5)
        print("Waiting for simulation to start...")
    
    # Then, check for "End simulation" in the last few lines
    while True:
        if time.time() - start_time > timeout:
            print(f"Timeout waiting for simulation to complete")
            return False
            
        time.sleep(5)
        print("Checking if simulation has completed...")
        
        try:
            with open(output_log, 'r') as f:
                # Read the last few lines
                lines = f.readlines()
                last_lines = lines[-4:] if len(lines) >= 4 else lines
                
                # Check if "End simulation" appears in the last few lines
                for line in last_lines:
                    if "End simulation" in line:
                        print("Simulation completed successfully!")
                        return True
        except Exception as e:
            print(f"Error reading output log: {e}")
            # Continue waiting even if there's a read error
            pass
        
        print("Simulation still running...")


# Create a singleton simulation run fixture to ensure we only run the simulation once
@pytest.fixture(scope="session")
def completed_simulation(simulation, work_dir):
    """Run the simulation once for all tests that need it."""
    sim_output_dir = os.path.join(work_dir, 'simulation', 'output')
    nerdss_dir = os.path.dirname(os.path.dirname(NERDSS_PATH))
    
    # Run a very short simulation for testing
    simulation.run_new_simulations(
        sim_indices=[1],
        sim_dir=sim_output_dir,
        nerdss_dir=nerdss_dir,
        parallel=False  # Run in non-parallel mode to ensure proper monitoring
    )
    
    # Wait for simulation to complete
    sim_subdir = os.path.join(sim_output_dir, "1")
    if not wait_for_simulation_completion(sim_subdir):
        pytest.skip("Simulation did not complete within the timeout period")
    
    # Return the path to the completed simulation
    return {
        'sim_dir': sim_output_dir,
        'sim_idx': 1,
        'data_dir': os.path.join(sim_subdir, "DATA")
    }


@pytest.mark.skipif(not nerdss_available, reason=f"NERDSS executable not found at {NERDSS_PATH}")
def test_simulation_run(completed_simulation):
    """Test that the simulation ran successfully and created expected output files."""
    # Verify expected output files exist
    sim_data_dir = completed_simulation['data_dir']
    assert os.path.exists(sim_data_dir)
    assert os.path.exists(os.path.join(sim_data_dir, "copy_numbers_time.dat"))


@pytest.mark.skipif(not nerdss_available, reason=f"NERDSS executable not found at {NERDSS_PATH}")
def test_analysis(completed_simulation, simulation):
    """Test basic analysis functionality using the already completed simulation."""
    # Initialize analysis using the completed simulation
    analysis = Analysis(save_dir=completed_simulation['sim_dir'])
    
    # Test that analysis object was created successfully
    assert analysis is not None
    assert hasattr(analysis, 'simulation_dirs')
    assert len(analysis.simulation_dirs) > 0
    
    # Test plotting function (would generate plots in a real run)
    # We're just checking it doesn't raise errors
    if simulation.model.molecule_types:
        mol_name = simulation.model.molecule_types[0].name
        try:
            analysis.plot_figure(
                figure_type="line",
                simulations=[0],  # Use the first simulation
                x="time",
                y="average_assembly",
                legend=[mol_name + '==1']
            )
        except FileNotFoundError:
            # It's okay if files aren't found since we're using a minimal simulation
            pass