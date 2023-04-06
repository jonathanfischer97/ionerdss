''''
This is just a workspace to test the speed of functions. Has some NERDSS output files as tests.

NERDSS Output File Explanation:
 - histogram_single_component: (Normally called histogram_complexes_time.dat) is a histogram of a single-component NERDSS sim.
 - histogram_multi_component: (Normally called histogram_complexes_time.dat) is a histogram of a multi-component NERDSS sim.
 - trajectory: i dont really know. I think shows the trajectories of the molecules in the simulation.
 - transition_matrix_time: idk
'''

from TestingFunctions.awful_tmr import badTimer
## CURRENTLY TESTING: hist.py
import numpy as np
import matplotlib.pyplot as plt
import ioNERDSS as ion





last = badTimer('Start',0)
ion.read_multi_hist(FileName='ioNERDSSPyPi\TestingFunctions\histogram_multi_component.dat',SpeciesList=['A','B'])
badTimer('start',last)



