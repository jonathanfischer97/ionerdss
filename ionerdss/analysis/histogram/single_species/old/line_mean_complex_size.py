import numpy as np
import matplotlib.pyplot as plt
from ..read_file import read_file


def line_mean_complex_size(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                 SpeciesName: str, ExcludeSize: int = 0, ShowFig: bool = True, SaveFig: bool = False):
    """Creates graph of the mean number of species in a single complex molecule over a time period.

    Args:
        FileName (str): Path to the histogram.dat file
        FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.
        ExcludeSize (int): Monomers in the complex that are smaller or equal to this number will not be included. 
        ShowFig (bool, optional): If the plot is shown. Defaults to True.
        SaveFig (bool, optional): If the plot is saved. Defaults to False.

    Returns:
        graph. X-axis = time. Y-axis = mean number of species in a single complex molecule.
    """
    
    #for file names
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    
    time_list = [] #list of every timestamp
    size_list = [] #list of mean sizes (index of this = index of timestep)

    for histogram_file_number in range(1, FileNum+1):
        
        #determining file name (if there are multiple or none)
        if FileNum == 1:
            temp_file_name = FileName
        else:
            temp_file_name = file_name_head + '_' + str(histogram_file_number) + '.' + file_name_tail

        total_size_list = [] #list of every timestamp for this file
        total_time_list = [] #list of mean sizes (index of this = index of timestep)
        
        #real file
        hist = read_file(temp_file_name, SpeciesName)
        
        #create list of means / timesteps, based on what sizes are excluded/not
        if ExcludeSize == 0:
            for timestep in hist:
                if InitialTime <= timestep[0] <= FinalTime:
                    total_time_list.append(timestep[0])
                    total_size_list.append(np.mean(timestep[2]))
        
        elif ExcludeSize > 0:
            for timestep in hist:
                if InitialTime <= timestep[0] <= FinalTime:
                    timestep_edited = [ele for ele in timestep[2] if ele>ExcludeSize] #create new list that only includes elements greater then exclude size
                    total_time_list.append(timestep[0])
                    total_size_list.append(np.mean(timestep_edited))
        else:
            print('ExcludeSize cannot smaller than 0!')
            return 0
        
        #add time/size lists to main, cross function lists
        time_list.append(total_time_list)
        size_list.append(total_size_list)
    
    #transpose list (each sub-list = 1 timesteps across every file)
    size_list_rev = []
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
        plt.title('Average Number of ' +
                  str(SpeciesName) + ' in Single Complex')
        plt.xlabel('Time (s)')
        plt.ylabel('Average Number of ' + str(SpeciesName))
        if SaveFig:
            plt.savefig('mean_complex.png', dpi=500)
        plt.show()
    return time_list[0], mean, 'Nan', std


