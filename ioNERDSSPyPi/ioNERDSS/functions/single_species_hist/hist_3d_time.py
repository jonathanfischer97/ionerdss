import numpy as np
import matplotlib.pyplot as plt
import warnings
from .hist_temp import hist_temp
from .read_file import read_file


def hist_3d_time(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                 SpeciesName: str, TimeBins: int, xBarSize: int = 1, ShowFig: bool = True, SaveFig: bool = False):
    """Takes in a histogram.dat file from NERDSS, and creates a 3D histogram that represents the average number of each complex size, over time.

    Args:
        FileName (str): Path to the histogram.dat file
        FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.
        TimeBins (int): The number of bins that the selected time period is divided into.
        xBarSize (int, optional): The size of each data bar in the x-dimension. Defaults to 1.
        ShowFig (bool, optional): If the plot is shown. Defaults to True.
        SaveFig (bool, optional): If the plot is saved. Defaults to False.

    Returns:
        Returns a 3D histogram representing the number of monomers in a single complex over time. X-axis = species type/size. Y-axis = averaged time. Z-axis = relative occurance.
    """




    warnings.filterwarnings('ignore')
    
    #creates equal time chunks b/w initial and final based on # of timebins
    t_arr = np.arange(InitialTime, FinalTime, (FinalTime-InitialTime)/TimeBins)
    t_arr = np.append(t_arr, FinalTime)
    
    #itilizing file name
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    
    z_list_tot = [] #list of present complex species for each time bin over all files
    x_list_tot = [] #list of average count of complex species for each timebin over all files
    
    
    for histogram_file_number in range(1, FileNum+1):
        
        #determining file name (if there are multiple or none)
        if FileNum == 1:
            temp_file_name = FileName
        else:
            temp_file_name = file_name_head + '_' + str(histogram_file_number) + '.' + file_name_tail

        max_num = 0 #biggest species over all timebins
        x_lst = [] #list of present complex species for each time bin
        z_lst = [] #list of average count of each complex species for each timebin
        t_plt = np.zeros(TimeBins) #creates a plot with sections = to # of time bins

        #load in the file
        hist = read_file(temp_file_name,SpeciesName)

        #for each time bin
        for time_index in range(0, len(t_arr)-1):
            t_plt[time_index] = (t_arr[time_index]+t_arr[time_index+1])/2 #have it so t_plt = the middle of each timebin
            
            #determine the present complex species + average count of them
            plot_conv, plot_count_mean = hist_temp(hist, t_arr[time_index], t_arr[time_index+1])
            
            x_lst.append(plot_conv)
            z_lst.append(plot_count_mean)
            
            #determine biggest species over all timebins
            if max(plot_conv) > max_num:
                max_num = max(plot_conv)
        
        z_plt = np.zeros(shape=(max_num, TimeBins)) #array to hold count of each species over each timebin w/ 0s
        
        #fills z_plt with z_lst and ranspose! (now each has a list of 1 complex species over each time_bin)
        for indexX,time_bin in enumerate(x_lst):
            for indexY,complex_species in enumerate(time_bin):
                z_plt[complex_species-1, indexX] = z_lst[indexX][indexY]

        #so the plot has correct sizes
        z_plt = z_plt.T #transpose back
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
        x_plt = np.arange(0, max_num, xBarSize)+1 #create list of species's sizes based, based on max size and bar size
        
        #append to main, cross file lists
        x_list_tot.append(x_plt)
        z_list_tot.append(list(z_plt_))
    
    #determine the largest species size across files
    max_x_num = 0
    for x_file in x_list_tot:
        if len(x_file) > max_x_num:
            max_x_num = len(x_file)
            n_list = x_file
    
    #ensure that the average count of specific species size list has equal length to the species type/size list
    for z_file in z_list_tot:
        for time_bin in z_file:
            if len(time_bin) < len(n_list):
                for k in range(0, 1 + len(n_list) - len(time_bin)):
                    time_bin.append(0.0)
    
    #determine mean count of species sizes in a time bin over each file
    count_list_mean = np.zeros([TimeBins, len(n_list)])
    for complex_species_index in range(len(z_list_tot[0])):
        for time_bin_index in range(len(z_list_tot[0][0])):
            temp_list = []
            for file_index in range(len(z_list_tot)):
                temp_list.append(z_list_tot[file_index][complex_species_index][time_bin_index])
            count_list_mean[complex_species_index][time_bin_index] += np.mean(temp_list)
    
    #show figure
    if ShowFig:
        xx, yy = np.meshgrid(n_list, t_plt)
        X, Y = xx.ravel(), yy.ravel()
        Z = np.array(count_list_mean.ravel())
        bottom = np.zeros_like(Z)
        width = xBarSize
        depth = 1/TimeBins
        fig = plt.figure()
        ax = fig.add_subplot(2,2,1,projection="3d")
        ax.bar3d(X, Y, bottom, width, depth, Z, shade=True)
        ax.set_xlabel('Number of ' + SpeciesName + ' in sigle complex')
        ax.set_ylabel('Time (s)')
        ax.set_zlabel('Count')
        if SaveFig:
            plt.savefig('histogram_3D.png', dpi=500)
        plt.show()
    return n_list, t_plt, count_list_mean, 'Nan'


