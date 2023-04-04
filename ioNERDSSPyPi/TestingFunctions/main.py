''''
This is just a workspace to test the speed of functions. Has some NERDSS output files as tests.

NERDSS Output File Explanation:
 - histogram_single_component: (Normally called histogram_complexes_time.dat) is a histogram of a single-component NERDSS sim.
 - trajectory: i dont really know. I think shows the trajectories of the molecules in the simulation.

'''

from awful_tmr import badTimer
## CURRENTLY TESTING: hist.py
def traj_track(FileName: str, SiteNum: int, MolIndex: list):
    array = []
    for i in range(len(MolIndex)):
        array.append([])
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:11] == 'iteration: ':
                index = 0
            if len(line.strip(' ').strip('\n').split()) == 4:
                if (index//SiteNum)+1 in MolIndex and index % SiteNum == 0:
                    info = line.strip(' ').strip('\n').split()
                    x = float(info[1])
                    y = float(info[2])
                    z = float(info[3])
                    coord = [x, y, z]
                    list_index = MolIndex.index((index//SiteNum)+1)
                    array[list_index].append(coord)
                index += 1
    return array


# -------------------------------------Gag (Sphere) Regularization Index Calculation---------------------------------------

# ref: https://jekel.me/2015/Least-Squares-Sphere-Fit/




last = badTimer('Start',0)

traj_track(FileName='ioNERDSSPyPi\TestingFunctions\\trajectory.xyz',SiteNum=7,MolIndex=[1])

badTimer('end',last)



