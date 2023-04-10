''''
This is just a workspace to test the speed of functions. Has some NERDSS output files as tests.

NERDSS Output File Explanation:
 - histogram_single_component: (Normally called histogram_complexes_time.dat) is a histogram that shows the number of each type (type = how many monomers are in it) 
 of complex molecule at every time step in single-component NERDSS sim.
 - histogram_multi_component: (Normally called histogram_complexes_time.dat) is a histogram that shows the number of each type (type = how many monomers of each type are in it) 
 of complex molecule at every time step in multi-component NERDSS sim.
 - trajectory: i dont really know. I think shows the trajectories of the molecules in the simulation.
 - transition_matrix_time: idk
 - database.pdb: describes the atoms / residuals of a protein. Comes from a protein database
 - nerdss_output.pdb: describes protiens (com, edges). Comes from NERDSS.
'''

from TestingFunctions.awful_tmr import badTimer
## CURRENTLY TESTING: hist.py
import ioNERDSS as ion






last = badTimer('Start',0)
lst = []
for i in range(0,50):
    lst.append(i)

print(lst)
ion.locate_position_PDB("ioNERDSSPyPi\TestingFunctions\\nerdss_output.pdb",[12],"ioNERDSSPyPi\TestingFunctions\parm.inp")
badTimer('Start',last)