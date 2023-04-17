import numpy as np
import matplotlib.pyplot as plt
from .read_multi_hist import read_multi_hist
from .list_index_exists import list_index_exists


def multi_max_complex(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                      SpeciesList: list, SpeciesName: str, ShowFig: bool = True, SaveFig: bool = False):
    """Creates a graph from a histogram.dat (multi-species) that shows the maximum number of selected monomers in a single complex molecule over a certain time period

    Args:
        FileName (str): Path to the histogram.dat file
        FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesList (list): The names of the species you want to examine. Should be in the .dat file.
        SpeciesName (str): The name of the specific species you want to examine. Should be in the .dat file.
        ShowFig (bool, optional): Whether to display the generated figures. Default is True.
        SaveFig (bool, optional): Whether to save the generated figures. Default is False.

    Returns:
        Graph. X-axis = Time. Y-axis =  maximum number of selected monomers in a single complex molecule.
    """
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    time_list = []
    size_list = []

    #runs through every file
    for histogram_file_number in range(1, FileNum+1):
        
        #determining file name (if there are multiple or none)
        if FileNum == 1:
            temp_file_name = FileName
        else:
            temp_file_name = file_name_head + '_' + str(histogram_file_number) + '.' + file_name_tail
        
        total_size_list = [] #list of max size at each at each time intervel (1 file)
        total_time_list = [] #time at each time interval (1 file)

        #get info from file
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)
        
        #go through each timestep in the file
        for time_step in hist_list:
            if time_step != []:
                time = time_step[0]
                if InitialTime <= time <= FinalTime:

                    #append time to time list
                    total_time_list.append(time)
                    max_size = 0

                    #go through each protein complex in this timestep
                    for protein_complex in time_step[1:]:
                        if SpeciesName == 'tot':
                            if max_size < np.sum(protein_complex[0:-1]): max_size = np.sum(protein_complex[0:-1])
                        elif SpeciesName in SpeciesList:
                            name_index = SpeciesList.index(SpeciesName)
                            if max_size < protein_complex[name_index]: max_size = protein_complex[name_index]
                        else:
                            print('SpeciesName not in SpeciesList!')
                            return 0
                    total_size_list.append(max_size)
        
        #append lists from this file, to the big list of all files
        size_list.append(total_size_list)
        time_list.append(total_time_list)
    
    #make it so each list include timesteps from each file, instead of each list being every timestep from a file.
    size_list_rev = []
    #Make it so each sub-list has the same timestamps from every file, sintead of having every timestamp from 1 file.
    for file in size_list:
        for indexY,size in enumerate(file):
            if not list_index_exists(size_list_rev,indexY):
                size_list_rev.append([])
            size_list_rev[indexY].append(size)

    #creates lists of means and stds
    mean = []
    std = []

    #runs through each timestamp and calculates means/stds
    for index,timestamps in enumerate(size_list_rev):
        
        #if this timestamp is equal to previous, copy previous. 
        if timestamps == size_list_rev[index-1]:
            mean.append(mean[index-1])
            if FileNum > 1: std.append(std[index-1])
        
        #Else calculate new measns/stds
        else:
            mean.append(np.nanmean(timestamps))
            if FileNum > 1: std.append(np.nanstd(timestamps))
    

    #find time that is equal to the length of means (or the longest time generally)
    time_index = -1
    for index,file in enumerate(time_list):
        if len(mean) == len(file):
            time_index = index
            break
    if time_index == -1:
        print('Times do not line up to means')
        return 0

    #create figure
    if ShowFig:
        errorbar_color = '#c9e3f6'
        plt.plot(time_list[time_index], mean, color='C0')
        if FileNum > 1:
            plt.errorbar(time_list[time_index], mean, color='C0',
                         yerr=std, ecolor=errorbar_color)
        if SpeciesName == 'tot':
            title_spec = 'Total Species'
        else:
            title_spec = SpeciesName
        plt.title('Maximum Number of ' +
                  str(title_spec) + ' in Single Complex')
        plt.xlabel('Time (s)')
        plt.ylabel('Maximum Number of ' + str(title_spec))
        if SaveFig:
            plt.savefig('multi_max_complex.png', dpi=500)
        plt.show()
    return time_list[time_index], mean, 'Nan', std


