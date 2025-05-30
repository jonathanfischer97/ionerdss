==============================
ionerdss (v.1.1) Documentation
==============================

:Date: 2025-03-22

.. note::

   This page does not include the outputs. To see the outputs, please refer to this `Jupyter notebooks <quick_start.html>`_.

.. code-block:: python

   import ionerdss as ion

Creating NERDSS Inputs
----------------------

This section describes how to automatically create inputs for NERDSS from a PDB structure.

.. code-block:: python

   import subprocess
   from IPython.display import display, Image

   pdb_id = '8y7s' # PDB ID for the structure of interest, or the full path to a PDB file
   save_folder = '~/Documents/8y7s_dir' # the working directory

   # create the PDBModel object using the PDBModel class
   pdb_model = ion.PDBModel(pdb_id=pdb_id, save_dir=save_folder)

   # coarse grain each chain of the PDB structure to a NERDSS molecule
   # set standard_output=True to see the determined interfaces
   pdb_model.coarse_grain(distance_cutoff=0.35, 
                        residue_cutoff=3,
                        show_coarse_grained_structure=False, 
                        save_pymol_script=False, 
                        standard_output=False)

   # regularize homologous chains to the same NERDSS molecule type
   pdb_model.regularize_homologous_chains(dist_threshold_intra=3.5, 
                                       dist_threshold_inter=3.5, 
                                       angle_threshold=25.0, 
                                       show_coarse_grained_structure=False, 
                                       save_pymol_script=True, 
                                       standard_output=False)

   # display the coarse-grained structure of the PDB model and the original PDB structure
   # requires PyMOL to be installed
   if save_folder.startswith('~'):
      abs_save_folder = os.path.expanduser(save_folder)
   abs_save_folder = os.path.abspath(abs_save_folder)

   subprocess.run(["pymol", "-cq", f"{abs_save_folder}/visualize_regularized_coarse_grained.pml"], check=True)
   display(Image(filename=f"{abs_save_folder}/comparison_regularized.png"))

Running NERDSS Simulations
--------------------------

This section describes how to run NERDSS simulations from ionerdss.

.. code-block:: python

   # create the Simulation object using the Simulation class
   # the simulation is connected to the PDBModel object created above
   simulation = ion.Simulation(pdb_model, save_folder)

   # generate the NERDSS input files for the simulation
   simulation.generate_nerdss_input()

   # example of modifying simulation parameters
   # all parameters can be modified using the modify_mol_file() and modify_inp_file()
   simulation.modify_mol_file('A', 
                              {'D': [20.0, 20.0, 20.0], 
                              'Dr': [0.2, 0.2, 0.2]})

   simulation.print_mol_parameters('A')

   simulation.modify_inp_file({'nItr': 1000, 'timeStep': 0.5, 
                              'timeWrite': 100, 'trajWrite': 100, 
                              'pdbWrite': 100, 'A': 200, 
                              'A(A1) + A(A1) <-> A(A1!1).A(A1!1)': {'onRate3Dka': 2000}})
   simulation.print_inp_file()

   # install NERDSS if not already installed
   simulation.install_nerdss(nerdss_path="~/Documents/8y7s_dir")

   # run the NERDSS simulation
   simulation.run_new_simulations(sim_indices=[1, 2, 3], 
                              sim_dir="~/Documents/8y7s_dir/nerdss_output", 
                              nerdss_dir="~/Documents/8y7s_dir/NERDSS", 
                              parallel=False)
   # this will run the simulation for 3 different random seeds
   # and save the outputs in the specified directory
   # check the simulation output to see if the simulations are run successfully
   # if the simulations are not run successfully, you have to run it manually in terminal

Analyzing NERDSS Outputs
------------------------

This section describes how to automatically analyze outputs for NERDSS simulation.

.. code-block:: python

   # create the Analysis object using the Analysis class
   # the nerdss_output directory is the output directory from the NERDSS simulation
   # it can be the parent directory of several simulations
   analysis = ion.Analysis("./data/8y7s_dir/nerdss_output/")

   # generate the trajecotry from the xyz file
   # if multiple simulations are provided, the random one will be selected
   # you can ignore the conflict about the PyQt6 and PySide6
   analysis.visualize_trajectory()

   # generate all types of plots using the plot_figure() method
   # the figure_type can be 'line', 'hist', '3dhist', 'heatmap'

   # plot the species copy number over time
   # all individual simulations and averaged result are plotted
   analysis.plot_figure(figure_type='line',
                     x='time',
                     y='species',
                     legend=[['A(A1!1).A(A1!1)'],],
                     show_type='both')

   # only plot the average result
   analysis.plot_figure(figure_type='line',
                     x='time',
                     y='species',
                     legend=[['A(A1!1).A(A1!1)'],],
                     show_type='average')

   # only plot the individual simulation results
   analysis.plot_figure(figure_type='line',
                     x='time',
                     y='species',
                     legend=[['A(A1!1).A(A1!1)'],],
                     show_type='individuals')

   # plot multiple species copy numbers over time
   # legend is a list of lists, where each inner list corresponds to a different plot
   # if multiple terms in the inner list are provided, their sum will be plotted
   analysis.plot_figure(figure_type='line',
                     x='time',
                     y='species',
                     legend=[['A(A1!1).A(A1!1)'], ['A(A1!1).A(A1!1)', 'A(A2!1).A(A2!1)', 'A(A3!1).A(A3!1)'],],
                     show_type='average')

   # plot the largest assembly size over time
   # plot the average
   analysis.plot_figure(figure_type='line',
                     x='time',
                     y='maximum_assembly',
                     legend=['A',],
                     show_type='average')

   # plot the average and individual simulation results
   analysis.plot_figure(figure_type='line',
                     x='time',
                     y='maximum_assembly',
                     legend=['A',],
                     show_type='both')

   # plot the average assembly size over time for assemblies >= 2
   analysis.plot_figure(figure_type='line',
                     x='time',
                     y='average_assembly',
                     legend=['A>=2'],
                     show_type='average')

   # plot the fraction of monomers in assemblies >= 4
   analysis.plot_figure(figure_type='line',
                     x='time',
                     y='fraction_of_monomers_assembled',
                     legend=['A>=4'],
                     show_type='average')

   # plot the histogram of assembly size of the whole simulation
   # can specify time_frame to plot the histogram of a specific time frame
   # frequency=True will plot the frequency of each assembly size
   # normalize=True will plot the normalized histogram (i.e., the area under the histogram equals 1)
   # set y='monomer_count' will plot the histogram of monomer count in the complex instead of complex count
   analysis.plot_figure(figure_type='hist', x='size', 
                     y='complex_count', legend=['A'], 
                     bins=10, frequency=False, normalize=False)

   # plot the 3d histogram of assembly size, time, and complex count / monomer count
   analysis.plot_figure(figure_type='3dhist', 
                        x='size', y='time', z='complex_count', 
                        legend=['A'], bins=10, time_bins=5, 
                        frequency=False, normalize=False, figure_size=(12, 12))

   # plot the heatmap of assembly size, time, and complex count / monomer count
   analysis.plot_figure(figure_type='heatmap', 
                        x='size', y='time', z='complex_count', 
                        legend=['A'], bins=10, time_bins=5, 
                        frequency=False, normalize=False, figure_size=(8, 6))

   # plot the free energy of assembly size
   analysis.plot_figure(figure_type='line', x='size', y='free_energy', 
                        legend=['A'], figure_size=(8, 6))

   # plot the symmetric association probability of assembly size
   # n-size + m-size -> n+m-size will be counted both for n-size and m-size 
   analysis.plot_figure(figure_type='line', 
                        x='size', y='symmetric_association_probability', 
                        legend=["associate size > 2", "associate size = 2", "associate size < 2"], 
                        show_type='average', figure_size=(8, 6))

   # plot the asymmetric association probability of assembly size
   # n-size + m-size -> n+m-size will be counted only for the larger size
   analysis.plot_figure(figure_type='line', 
                        x='size', y='asymmetric_association_probability', 
                        legend=["associate size > 2", "associate size = 2", "associate size < 2"], 
                        show_type='average', figure_size=(8, 6))

   # plot the symmetric dissociation probability of assembly size
   # n+m-size -> n-size + m-size will be counted both for n-size and m-size
   analysis.plot_figure(figure_type='line', 
                        x='size', y='symmetric_dissociation_probability', 
                        legend=["dissociate size > 2", "dissociate size = 2", "dissociate size < 2"], 
                        show_type='average', figure_size=(8, 6))

   # plot the asymmetric dissociation probability of assembly size
   # n+m-size -> n-size + m-size will be counted only for the smaller dissociation size
   analysis.plot_figure(figure_type='line', 
                        x='size', y='asymmetric_dissociation_probability', 
                        legend=["dissociate size > 2", "dissociate size = 2", "dissociate size < 2"], 
                        show_type='average', figure_size=(8, 6))

   # plot the growth probability of assembly size
   analysis.plot_figure(figure_type='line', 
                        x='size', y='growth_probability', 
                        legend=["A"], show_type='average', figure_size=(8, 6))

   # plot the lifetime of assembly size
   analysis.plot_figure(figure_type='line', 
                        x='size', y='lifetime', 
                        legend=["A"], show_type='average', figure_size=(8, 6))

   # examples for multispecies analysis
   # create the Analysis object for the 8erq simulation (hetero-trimer assembly)
   analysis_8erq = ion.Analysis("./data/8erq_dir/nerdss_output/")

   analysis_8erq.plot_figure(figure_type='line',
                     x='time',
                     y='species',
                     legend=[['C(A1!1).A(C1!1)'],],
                     show_type='average')

   analysis_8erq.plot_figure(figure_type='line',
                     x='time',
                     y='maximum_assembly',
                     legend=['A',],
                     show_type='both')

   analysis_8erq.plot_figure(figure_type='line',
                     x='time',
                     y='maximum_assembly',
                     legend=['B',],
                     show_type='both')

   # plot the maximum assembly size for both A and B species
   # y axis is the max of sum of A and B species in one complex
   analysis_8erq.plot_figure(figure_type='line',
                     x='time',
                     y='maximum_assembly',
                     legend=['A', 'B'],
                     show_type='both')

   # plot the average assembly size for both A and B species
   # y axis is the average of sum of A and B species in one complex
   # only include assemblies meeting the criteria in legend
   # e.g., A>=1 and B>=2 means only assemblies with at least 1 A and 2 B are included
   analysis_8erq.plot_figure(figure_type='line',
                     x='time',
                     y='average_assembly',
                     legend=['A>=1, B>=2'],
                     show_type='both')

   # here we plot the average assembly size for A and B species separately
   # the legend is a list of lists, where each inner list corresponds to a different plot
   # e.g., ['A>=1'] means only assemblies with at least 1 A are included
   # and ['B>=1'] means only assemblies with at least 1 B are included                     
   analysis_8erq.plot_figure(figure_type='line',
                     x='time',
                     y='average_assembly',
                     legend=['A>=1', 'B>=1'],
                     show_type='average')

   # plot the fraction of B monomers in assemblies B >= 3 
   analysis_8erq.plot_figure(figure_type='line',
                     x='time',
                     y='fraction_of_monomers_assembled',
                     legend=['B>=3'],
                     show_type='average')

   analysis_8erq.plot_figure(figure_type='hist', 
                              x='size', y='complex_count', 
                              legend=['B'], bins=10, frequency=False, normalize=False)

   analysis_8erq.plot_figure(figure_type='hist', 
                              x='size', y='monomer_count', 
                              legend=['B'], bins=10, frequency=True, normalize=False)

   analysis_8erq.plot_figure(figure_type='3dhist', 
                              x='size', y='time', z='complex_count', 
                              legend=['B'], bins=10, time_bins=5, 
                              frequency=False, normalize=False, figure_size=(12, 12))

   # plot the 3d histogram of one species assembly size, another species assembly size, and comlex count
   analysis_8erq.plot_figure(figure_type='heatmap', 
                              x='size', y='size', z='complex_count', 
                              legend=['A', 'B'], 
                              bins=10, frequency=False, normalize=False, figure_size=(8, 6))

   # plot the stacked histogram of assembly size and complex count for A and B species
   analysis_8erq.plot_figure(figure_type='stacked', 
                              x='size', y='complex_count', legend=["B: A<2, A=2, A>2"], 
                              bins=10, frequency=False, normalize=False, figure_size=(8, 6))
