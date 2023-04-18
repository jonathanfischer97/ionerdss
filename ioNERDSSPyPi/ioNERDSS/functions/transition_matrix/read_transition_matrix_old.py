import numpy as np


def read_transition_matrix_old(FileName: str, SpeciesName: str, InitialTime: float, FinalTime: float):
    """
    Parses transition_matrix_time.dat, and returns the matrices at two given time points.

    Args:
        FileName (str): The name of the file to be read.
        SpeciesName (str): The name of the species to be analyzed.
        InitialTime (float): The initial time point of interest.
        FinalTime (float): The final time point of interest.

    Returns:
          A tuple that contains:
           - NumPy array of the transition matrix at the initial time point
           - NumPy array of the transition matrix at the final time point
    """
    ti_switch = False
    tf_switch = False
    spec_switch = False
    ti_matrix = []
    tf_matrix = []
    with open(FileName, 'r') as file:
        
        #for each line
        for line in file.readlines():
            
            #checks the time. If it is equal to initial/final, start reading ti/tf
            if line[0:5] == 'time:':
                if float(line.split(' ')[1]) == InitialTime:
                    ti_switch = True
                if float(line.split(' ')[1]) == FinalTime:
                    tf_switch = True
                if float(line.split(' ')[1]) != InitialTime:
                    ti_switch = False
                if float(line.split(' ')[1]) != FinalTime:
                    tf_switch = False
            
            #if lifetime or size is hit, stop reading everything
            if line[0:8] == 'lifetime':
                ti_switch = False
                tf_switch = False
                spec_switch = False
            if line[0:4] == 'size':
                ti_switch = False
                tf_switch = False
                spec_switch = False
            
            #if speciesname is hit, start reading species
            if line[0:4] == SpeciesName:
                spec_switch = True
            
            #if species + time initial are read, read and add it to time initial matrix
            if ti_switch and spec_switch:
                if line != SpeciesName + '\n':
                    info = line.strip(' ').strip('\n').split(' ')
                    temp_list = []
                    for value in info:
                        temp_list.append(int(value))
                    ti_matrix.append(temp_list)
            
            #if species + time final are read, read and add it to time final matrix
            if tf_switch and spec_switch:
                if line != SpeciesName + '\n':
                    info = line.strip(' ').strip('\n').split(' ')
                    temp_list = []
                    for value in info:
                        temp_list.append(int(value))
                    tf_matrix.append(temp_list)
    ti_matrix = np.array(ti_matrix)
    tf_matrix = np.array(tf_matrix)
    return ti_matrix, tf_matrix


