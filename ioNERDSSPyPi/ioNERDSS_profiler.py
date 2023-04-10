''''
This is just a workspace to test the speed of functions. Has some NERDSS output files as tests.

NERDSS Output File Explanation:
 - histogram_single_component: (Normally called histogram_complexes_time.dat) is a histogram that shows the number of each type (type = how many monomers are in it) 
 of complex molecule at every time step in single-component NERDSS sim.
 - histogram_multi_component: (Normally called histogram_complexes_time.dat) is a histogram that shows the number of each type (type = how many monomers of each type are in it) 
 of complex molecule at every time step in multi-component NERDSS sim.
 - trajectory: i dont really know. I think shows the trajectories of the molecules in the simulation.
 - transition_matrix_time: idk
 - 1si4.pdb: describes info about hemogoblin??? (wow this list is not super helpful is it)
'''

from TestingFunctions.awful_tmr import badTimer
## CURRENTLY TESTING: hist.py
import numpy as np
import matplotlib.pyplot as plt
import ioNERDSS as ion






last = badTimer('Start',0)

newProtein = ion.ProteinComplex('ioNERDSSPyPi\TestingFunctions\\1si4.pdb',['A','B'])
"""newProtein.calc_angle()
newProtein.set_COM()
newProtein.filter(['A','B'])
newProtein.set_sigma()
newProtein.write_new_input()
newProtein.show_3D_graph()
newProtein.write_new_PDB()"""



badTimer('Start',last)