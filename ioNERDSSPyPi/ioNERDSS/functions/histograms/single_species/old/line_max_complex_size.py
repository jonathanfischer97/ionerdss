import numpy as np
import matplotlib.pyplot as plt
from ..read_file import read_file


def line_max_complex_size(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                SpeciesName: str, ShowFig: bool = True, SaveFig: bool = False):
    """Creates graph of the max number of species in a single complex molecule over a time period.

    Args:
        FileName (str): Path to the histogram.dat file
        FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.
        ShowFig (bool, optional): If the plot is shown. Defaults to True.
        SaveFig (bool, optional): If the plot is saved. Defaults to False.

    Returns:
        graph. X-axis = time. Y-axis = max number of species in a single complex molecule.
    """
    
    #init names
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    
    time_list = [] #list of every timestamp
    size_list = [] #list of max sizes (index of this = index of timestep)
    
    
    for histogram_file_number in range(1, FileNum+1):
        
        #determining file name (if there are multiple or none)
        if FileNum == 1:
            temp_file_name = FileName
        else:
            temp_file_name = file_name_head + '_' + str(histogram_file_number) + '.' + file_name_tail
        
        total_size_list = [] #list of every timestep (for this file)
        total_time_list = [] #list of max sizes (for this file)
        
        #read histogram
        hist = read_file(temp_file_name, SpeciesName)
        
        #for each timestep determine the time + max size
        for timestep in hist:
            if InitialTime <= timestep[0] <= FinalTime:
                total_time_list.append(timestep[0])
                total_size_list.append(np.max(timestep[2]))
        
        #append data to main, cross file lists
        time_list.append(total_time_list)
        size_list.append(total_size_list)
    
    #transpose list (each sub-list = 1 timesteps across every file)
    size_list_rev = np.transpose(size_list)
   
   #find mean and std dev
    mean = []
    std = []

    for index,timestamps in enumerate(size_list_rev):
        
        #if this timestamp is equal to previous, copy previous. 
        if timestamps == size_list_rev[index-1]:
            mean.append(mean[index-1])
            if FileNum > 1: std.append(std[index-1])
        
        #Else calculate new measns/stds
        else:
            mean.append(np.nanmean(timestamps))
            if FileNum > 1: std.append(np.nanstd(timestamps))
    
    #show figure
    if ShowFig:
        errorbar_color = '#c9e3f6'
        plt.plot(time_list[0], mean, color='C0')
        if FileNum > 1:
            plt.errorbar(time_list[0], mean, color='C0',
                         yerr=std, ecolor=errorbar_color)
        plt.title('Maximum Number of ' +
                  str(SpeciesName) + ' in Single Complex')
        plt.xlabel('Time (s)')
        plt.ylabel('Maximum Number of ' + str(SpeciesName))
        if SaveFig:
            plt.savefig('max_complex.png', dpi=500)
        plt.show()
    return time_list[0], mean, 'Nan', std


