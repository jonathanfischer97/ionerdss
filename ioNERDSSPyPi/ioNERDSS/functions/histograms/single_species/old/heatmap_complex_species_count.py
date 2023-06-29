import numpy as np
import matplotlib.pyplot as plt
from ..hist_temp import hist_temp
from ..read_file import read_file


def heatmap_complex_species_count(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                      SpeciesName: str, TimeBins: int, xBarSize: int = 1, ShowFig: bool = True,
                      ShowMean: bool = False, ShowStd: bool = False, SaveFig: bool = False):
    """Creates a 2D Heatmap from a histogram.dat file that represents the average number of each complex size, over time.

    Args:
        FileName (str): file location (relative) histogram.dat that will be read
        FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.        T
        TimeBins (int): The number of bins that the selected time period is divided into.
        xBarSize (int, optional): The size of each data bar in the x-dimension. Defaults to 1.
        ShowFig (bool, optional): If the plot is shown. Defaults to True.
        ShowMean (bool, optional): If means will be shown in each box. Defaults to False.
        ShowStd (bool, optional): If std values will be shown in each box. Defaults to False.
        SaveFig (bool, optional): If the plot is saved. Defaults to False.

    Returns:
        2D heatmap. X-axis: size of complex species. Y-axis = time 'bins'. Color = relative number of each species.
    """
    
    #creates equal time chunks b/w initial and final based on # of timebins
    t_arr = np.arange(InitialTime, FinalTime, (FinalTime-InitialTime)/TimeBins)
    t_arr = np.append(t_arr, FinalTime)
    
    #initilize file name
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    
    z_list_tot = [] #list of list of each complex type/size. Each sublist = file. Subsublist = timebin.
    x_list_tot = [] #list of list of average count of each complex type/size. Each sublist = file. Subsublist = timebin.
    
    for histogram_file_number in range(1, FileNum+1):
        
        #determining file name (if there are multiple or none)
        if FileNum == 1:
            temp_file_name = FileName
        else:
            temp_file_name = file_name_head + '_' + str(histogram_file_number) + '.' + file_name_tail
        
        max_num = 0 #largest complex size
        x_lst = [] #list of list of each complex type/size. Each sublist = time bin
        z_lst = [] #list of list of average count of each complex type/size. Each sublist = time bin
        t_plt = [] #main plot
        
        #load in the file
        hist = read_file(temp_file_name,SpeciesName)
        
        #for each timebin
        for time_bin in range(0, len(t_arr)-1):
            
            #initilize time plot for this timebin
            t_plt.append(str(round(t_arr[time_bin], 2)) +
                         's ~ ' + str(round(t_arr[time_bin+1], 2)) + 's')
            
            #get values for this time bin
            x, z = hist_temp(hist, t_arr[time_bin], t_arr[time_bin+1],)
            x_lst.append(x)
            z_lst.append(z)
            if max(x) > max_num:
                max_num = max(x)
        
        #initilize main plot
        z_plt = np.zeros(shape=(max_num, TimeBins))
        
        #puts values into main plot and transpose (now each has a list of 1 complex species over each time_bin))
        for timebin_index,timebin in enumerate(x_lst):
            for protein_index,protein_complex in enumerate(timebin):
                z_plt[protein_complex-1, timebin_index] = z_lst[timebin_index][protein_index]
        
        #transpose back
        z_plt = np.array(z_plt).T
        z_plt_ = []

        for time_bin in z_plt:
            z_plt_temp = []
            x_count = 0
            sum_ = 0.0
            
            #for each complex species type, if the barsize is >1 then add together different time bins
            for index,complex_species in enumerate(time_bin):
                x_count += 1
                sum_ += complex_species
                if index == len(z_plt) - 1:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
                elif x_count == xBarSize:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
            z_plt_.append(z_plt_temp)
        z_plt_ = np.array(z_plt_)
        x_plt = np.arange(0, max_num, xBarSize)+1 #creates x_plt that holds each species tyoe

        
        #append to main, cross file lists 
        x_list_tot.append(x_plt)
        z_list_tot.append(list(z_plt_))
    
    #determine largest complex species
    max_x_num = 0
    for file in x_list_tot:
        if len(file) > max_x_num:
            max_x_num = len(file)
            n_list = file
    
    #ensure that the average count of specific species size list has equal length to the species type/size list
    for file in z_list_tot:
        for time_bin in file:
            if len(time_bin) < len(n_list):
                for na in range(0, 1 + len(n_list) - len(time_bin)):
                    time_bin.append(0.0)
    
    #determine mean count / std of species sizes in a time bin over each file
    count_list_mean = np.zeros([TimeBins, len(n_list)])
    count_list_std = np.zeros([TimeBins, len(n_list)])
    for i in range(len(z_list_tot[0])):
        for j in range(len(z_list_tot[0][0])):
            temp_list = []
            for k in range(len(z_list_tot)):
                temp_list.append(z_list_tot[k][i][j])
            count_list_mean[i][j] += np.mean(temp_list)
            count_list_std[i][j] += np.std(temp_list)
    
    #show figure
    if ShowFig:
        fig, ax = plt.subplots()
        im = ax.imshow(count_list_mean)
        ax.set_xticks(np.arange(len(n_list)))
        ax.set_yticks(np.arange(len(t_plt)))
        ax.set_xticklabels(n_list)
        ax.set_yticklabels(t_plt)
        if ShowMean and ShowStd:
            print('Cannot show both maen and std!')
            return 0
        if ShowMean:
            for i in range(len(t_plt)):
                for j in range(len(n_list)):
                    text = ax.text(j, i, round(
                        count_list_mean[i, j], 1), ha='center', va='center', color='w')
        elif ShowStd and FileNum != 1:
            for i in range(len(t_plt)):
                for j in range(len(n_list)):
                    text = ax.text(j, i, round(
                        count_list_std[i, j], 1), ha='center', va='center', color='w')
        ax.set_title('Size distribution with Changing of Time')
        fig.tight_layout()
        plt.colorbar(im)
        plt.xlabel('Size of Complex')
        plt.ylabel('Time (s)')
        if SaveFig:
            plt.savefig('hist_heatmap.png', dpi=500, bbox_inches='tight')
        plt.show()
    return n_list, t_plt, count_list_mean, count_list_std


