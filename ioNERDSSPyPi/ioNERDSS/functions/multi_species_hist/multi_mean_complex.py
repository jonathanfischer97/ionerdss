import numpy as np
import matplotlib.pyplot as plt
from .read_multi_hist import read_multi_hist

def badTimer(event,last):
    
    #find the current time
    import time 
    current = time.perf_counter()
    
    #print which event is running
    print(f'\nEvent: {event}')

    #print how long since previous time
    if not last == 0:
        print(f'Time to Run: {current-last}')
    

    #update last time
    last = current
    return last


def multi_mean_complex(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                       SpeciesList: list, SpeciesName: str, ExcludeSize: int = 0, ShowFig: bool = True, SaveFig: bool = False):
    """Creates a graph from a histogram.dat (multi-species) that shows the mean number of selected monomers in a single complex molecule over a certain time period

    Args:
        FileName (str): Path to the histogram.dat file
        FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesList (list): The names of the species you want to examine. Should be in the .dat file.
        SpeciesName (str): The name of the specific species you want to examine. Should be in the .dat file.
        ExcludeSize (int, optional): The minimum value required to include a data point in the histogram. Default is 0.
        ShowFig (bool, optional): Whether to display the generated figures. Default is True.
        SaveFig (bool, optional): Whether to save the generated figures. Default is False.

    Returns:
        Graph. X-axis = Time. Y-axis =  mean number of selected monomers in a single complex molecule.
    """
    if FileNum > 1:
        #if there are more than 1 files, this wil help get name
        file_name_head = FileName.split('.')[0]
        file_name_tail = FileName.split('.')[1]
    
    time_list = [] #list of lists of average sizes at timestamp (all files)
    size_list = [] #list of lists of each timestep (all files)
    
    #as each file, goes through and counts up sizes of complexes (number of proteins inside) + # of complexes
    for histogram_file_number in range(1, FileNum+1):
        
        #determining file name (if there are multiple or none)
        if FileNum == 1:
            temp_file_name = FileName
        else:
            temp_file_name = file_name_head + '_' + str(histogram_file_number) + '.' + file_name_tail

        total_size_list = [] #list of average sizes at timestamp (1 file)
        total_time_list = [] #list of each timestep (1 file)
       

        #creates a list. ([i][0] = time, [i][1+] = arrays that describe complex species, [i][1+][0:-1] = count of each species, [1][1+][-1] = count of that complex species)
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)

        #go through each time step and find
        for time_step in hist_list:
            if time_step != []: #if timestep exists
                time = time_step[0]
                if InitialTime <= time <= FinalTime: #if inside specific time
                    total_time_list.append(time)
                    temp_sum = 0 # number of proteins
                    count = 0 #number of complexes

                    #Counts up the size of each complex (based on inputted protein) / number of complexes
                    for protein_complex in time_step[1:]:
                        #each protein complex (list with # of proteins in that complex. Final number = number of complexes.)
                        if SpeciesName == 'tot':
                            total_size = sum(protein_complex[0:-1])
                        elif SpeciesName in SpeciesList:
                            name_index = SpeciesList.index(SpeciesName)
                            total_size = protein_complex[name_index]
                        else:
                            print('SpeciesName not in SpeciesList!')
                            return 0

                        if total_size >= ExcludeSize:
                            count += protein_complex[-1]
                            temp_sum += total_size * protein_complex[-1]
                    
                    #adds the average size at timestamp to list
                    if count != 0:
                        total_size_list.append(temp_sum/count)
                    else:
                        total_size_list.append(0.0)

        #adds this files size/time lists to a master list
        size_list.append(total_size_list)
        time_list.append(total_time_list)


    #Make it so each sub-list has the same timestamps from every file, sintead of having every timestamp from 1 file.
    size_list_rev = np.transpose(size_list)
    

    #creates lists of means and stds
    mean = np.array([])
    std = np.array([])

    #runs through each timestamp and calculates means/stds
    for index,timestamps in enumerate(size_list_rev):
        
        #if this timestamp is equal to previous, copy previous. 
        if timestamps == size_list_rev[index-1]:

            mean = np.append(mean,mean[index-1])
            if FileNum > 1: std = np.append(std,std[index-1])
        
        #Else calculate new measns/stds
        else:
            mean = np.append(mean,np.nanmean(timestamps))
            if FileNum > 1: std = np.append(std,np.nanstd(timestamps))


    #create figure
    if ShowFig:
        errorbar_color = '#c9e3f6'
        plt.plot(time_list[0], mean, color='C0')
        if FileNum > 1:
            plt.errorbar(time_list[0], mean, color='C0',
                         yerr=std, ecolor=errorbar_color)
        if SpeciesName == 'tot':
            title_spec = 'Total Species'
        else:
            title_spec = SpeciesName
        plt.title('Mean Number of ' +
                  str(title_spec) + ' in Single Complex')
        plt.xlabel('Time (s)')
        plt.ylabel('Mean Number of ' + str(title_spec))
        if SaveFig:
            plt.savefig('multi_mean_complex.png', dpi=500)
        plt.show()
    return time_list[0], mean, 'Nan', std





#Old code replaced by np.transpose
"""size_list_rev = []
for i in range(len(size_list[0])):
    temp = []
    for j in range(len(size_list)):
        temp.append(size_list[j][i])
    size_list_rev.append(temp)
input(f"{size_list_rev}")"""