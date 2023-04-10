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
import math
import copy



"""def single_locate_position_restart(FileNamePdb, ComplexSize, FileNameRestart='restart.dat'):
    print('Reading restart.dat...')
    complex_lst = RESTART_read_restart(FileNameRestart)
    print('Reading files complete!')
    protein_remain = []
    for i in complex_lst:
        if len(i) == ComplexSize:
            protein_remain.append(i)
    protein_remain_flat = []
    for i in protein_remain:
        for j in i:
            protein_remain_flat.append(j)
    RESTART_new_pdb(FileNamePdb, protein_remain_flat)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0"""



last = badTimer('start',0)
ion.single_locate_position_restart('ioNERDSSPyPi\TestingFunctions\\nerdss_output.pdb',17,"ioNERDSSPyPi\TestingFunctions\\restart.dat")
badTimer('start',last)
#ioNERDSSPyPi\TestingFunctions\databse.pdb