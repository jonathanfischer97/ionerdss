''''
This is just a workspace to test the speed of functions. Has some NERDSS output files as tests.

NERDSS Output File Explanation:
 - histogram_single_component: (Normally called histogram_complexes_time.dat) is a histogram of a single-component NERDSS sim.
 - trajectory: i dont really know. I think shows the trajectories of the molecules in the simulation.
 - transition_matrix_time: idk
'''

from awful_tmr import badTimer
## CURRENTLY TESTING: hist.py
import numpy as np
import matplotlib.pyplot as plt
import warnings


def read_transition_matrix(FileName: str, SpeciesName: str, InitialTime: float, FinalTime: float):
    ti_switch = False
    tf_switch = False
    spec_switch = False
    ti_matrix = []
    tf_matrix = []
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:5] == 'time:':
                if float(line.split(' ')[1]) == InitialTime:
                    ti_switch = True
                if float(line.split(' ')[1]) == FinalTime:
                    tf_switch = True
                if float(line.split(' ')[1]) != InitialTime:
                    ti_switch = False
                if float(line.split(' ')[1]) != FinalTime:
                    tf_switch = False
            if line[0:8] == 'lifetime':
                ti_switch = False
                tf_switch = False
                spec_switch = False
            if line[0:4] == 'size':
                ti_switch = False
                tf_switch = False
                spec_switch = False
            if line[0:4] == SpeciesName:
                spec_switch = True
            if ti_switch and spec_switch:
                if line != SpeciesName + '\n':
                    info = line.strip(' ').strip('\n').split(' ')
                    temp_list = []
                    for i in info:
                        temp_list.append(int(i))
                    ti_matrix.append(temp_list)
            if tf_switch and spec_switch:
                if line != SpeciesName + '\n':
                    info = line.strip(' ').strip('\n').split(' ')
                    temp_list = []
                    for i in info:
                        temp_list.append(int(i))
                    tf_matrix.append(temp_list)
    ti_matrix = np.array(ti_matrix)
    tf_matrix = np.array(tf_matrix)
    return ti_matrix, tf_matrix


def dissociate_prob_asymmetric(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                               SpeciesName: str, DivideSize: int = 2, ShowFig: bool = True, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    matrix_list = []
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_matrix, tf_matrix = read_transition_matrix(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        matrix = tf_matrix - ti_matrix
        matrix_list.append(matrix)
    above = []
    equal = []
    below = []
    for k in range(len(matrix_list)):
        above_temp = np.zeros(len(matrix_list[0][0]))
        equal_temp = np.zeros(len(matrix_list[0][0]))
        below_temp = np.zeros(len(matrix_list[0][0]))
        i = 0
        while i < len(matrix_list[k][0]):
            j = 0
            while j < len(matrix_list[k][i]):
                if i > j:
                    if i % 2 == 0:
                        if j <= (i-1)/2:
                            if j + 1 == DivideSize:
                                equal_temp[i] += matrix_list[k][j][i]
                            elif j + 1 > DivideSize:
                                above_temp[i] += matrix_list[k][j][i]
                            else:
                                below_temp[i] += matrix_list[k][j][i]
                    else:
                        if j <= int(i/2):
                            if (i-1)/2 == j:
                                if j + 1 == DivideSize:
                                    equal_temp[i] += matrix_list[k][j][i]/2
                                elif j + 1 > DivideSize:
                                    above_temp[i] += matrix_list[k][j][i]/2
                                else:
                                    below_temp[i] += matrix_list[k][j][i]/2
                            else:
                                if j + 1 == DivideSize:
                                    equal_temp[i] += matrix_list[k][j][i]
                                elif j + 1 > DivideSize:
                                    above_temp[i] += matrix_list[k][j][i]
                                else:
                                    below_temp[i] += matrix_list[k][j][i]
                j += 1
            i += 1
        above.append(above_temp)
        equal.append(equal_temp)
        below.append(below_temp)
    above_prob = []
    equal_prob = []
    below_prob = []
    for i in range(len(above)):
        above_prob_temp = np.array([])
        equal_prob_temp = np.array([])
        below_prob_temp = np.array([])
        for j in range(len(above[0])):
            sum = above[i][j] + equal[i][j] + below[i][j]
            if sum != 0:
                above_prob_temp = np.append(above_prob_temp, above[i][j]/sum)
                equal_prob_temp = np.append(equal_prob_temp, equal[i][j]/sum)
                below_prob_temp = np.append(below_prob_temp, below[i][j]/sum)
            else:
                above_prob_temp = np.append(above_prob_temp, np.nan)
                equal_prob_temp = np.append(equal_prob_temp, np.nan)
                below_prob_temp = np.append(below_prob_temp, np.nan)
        above_prob.append(above_prob_temp)
        equal_prob.append(equal_prob_temp)
        below_prob.append(below_prob_temp)
    above_prob_rev = []
    for i in range(len(above_prob[0])):
        temp = []
        for j in range(len(above_prob)):
            temp.append(above_prob[j][i])
        above_prob_rev.append(temp)
    equal_prob_rev = []
    for i in range(len(equal_prob[0])):
        temp = []
        for j in range(len(equal_prob)):
            temp.append(equal_prob[j][i])
        equal_prob_rev.append(temp)
    below_prob_rev = []
    for i in range(len(below_prob[0])):
        temp = []
        for j in range(len(below_prob)):
            temp.append(below_prob[j][i])
        below_prob_rev.append(temp)
    mean_above = []
    mean_equal = []
    mean_below = []
    std_above = []
    std_equal = []
    std_below = []
    for i in range(len(above_prob_rev)):
        mean_above.append(np.nanmean(above_prob_rev[i]))
        mean_equal.append(np.nanmean(equal_prob_rev[i]))
        mean_below.append(np.nanmean(below_prob_rev[i]))
        if FileNum != 1:
            std_above.append(np.nanstd(above_prob_rev[i]))
            std_equal.append(np.nanstd(equal_prob_rev[i]))
            std_below.append(np.nanstd(below_prob_rev[i]))
    mean_above = np.nan_to_num(mean_above)
    mean_equal = np.nan_to_num(mean_equal)
    mean_below = np.nan_to_num(mean_below)
    n_list = list(range(1, 1 + len(matrix_list[0])))
    if ShowFig:
        errorbar_color_1 = '#c9e3f6'
        errorbar_color_2 = '#ffe7d2'
        errorbar_color_3 = '#d7f4d7'
        plt.plot(n_list, mean_above, 'C0')
        plt.plot(n_list, mean_equal, 'C1')
        plt.plot(n_list, mean_below, 'C2')
        if FileNum != 1:
            plt.errorbar(n_list, mean_above, yerr=std_above,
                         ecolor=errorbar_color_1, capsize=2)
            plt.errorbar(n_list, mean_equal, yerr=std_equal,
                         ecolor=errorbar_color_2, capsize=2)
            plt.errorbar(n_list, mean_below, yerr=std_below,
                         ecolor=errorbar_color_3, capsize=2)
        plt.legend(['Dissociate Size > ' + str(DivideSize), 'Dissociate Size = ' +
                    str(DivideSize), 'Dissociate Size < ' + str(DivideSize)])
        plt.xlabel('Number of ' + str(SpeciesName) + ' in Single Complex')
        plt.ylabel('Probability')
        plt.xticks(ticks=n_list)
        plt.title('Asymmetric Dissociation Probability')
        if SaveFig:
            plt.savefig('dissociate_probability_asymmetric.png', dpi=500)
        plt.show()
    return n_list, [mean_above, mean_equal, mean_below], 'Nan', [std_above, std_equal, std_below]









last = badTimer('Start',0)
dissociate_prob_asymmetric(FileName='ioNERDSSPyPi\TestingFunctions\\transition_matrix_time.dat',FileNum=1,InitialTime=0,FinalTime=1,SpeciesName='dode',ShowFig=True)
badTimer('start',last)



