import numpy as np


def single_hist_to_csv(FileName: str):
    """Creates a .csv (spreadsheet) file from a histogram.dat file (single-species)

    Args:
        FileName (str): Path to the histogram.dat file

    Returns:
        histogram.csv file: Each row is a different time stamp (all times listed in column A). Each column is a different size of complex molecule (all sizes listed in row 1). Each box 
        is the number of that complex molecule at that time stamp.
    """
    
    column_list = [] #holds the name of each column (Time + each complex name)
    time_list = [] #holds each time. Index corresponds to a sublist in name/size_list
    name_list = [] #holds each name for each datapoint. Index corresponds with size_list
    size_list = [] #holds each size for each datapoint. Index corresponds with name_list

    name_sub = [] #holds sublist of names. appended to name_list
    size_sub = [] #holds sublist of size. appended to size_list

    #Creates list with every complex type/size
    with open(FileName, 'r') as file:
        for index,line in enumerate(file.readlines()):
            
            #if it is a time stamp
            if line[0:9] == 'Time (s):':
                time_list.append(float(line.split(' ')[-1]))

                #if there was a previous timestamp before it that needs to be initilized
                if index != 0:
                    name_list.append(name_sub)
                    size_list.append(size_sub)
                    name_sub = []
                    size_sub = []
            else:
                
                #get name of species & get number of species in this complex
                name = line.split('	')[1].strip(' \n')
                name_sub.append(name)
                size_sub.append(int(line.split('	')[1].split(' ')[1].strip('.')))

                #creates a list of every 'name'
                if name not in column_list:
                    column_list.append(name)
    
    #at the end append the final subs because of the fence problem thing :(
    name_list.append(name_sub)
    size_list.append(size_sub) 
    column_list.sort()
    
    #write the file!
    with open('histogram.csv', 'w') as write_file:
        
        #create column names
        head = 'Time(s):'
        for column in column_list:
            head += ','
            head += column
        head += '\n'
        write_file.write(head)

        #write the bulk of the file
        for index,timestep in enumerate(time_list):
            
            #initilize writing
            write = ''

            #write time to string
            write += f"{str(timestep)}"

            #write data to string
            for column in column_list:
                write += ','
                if column in name_list[index]:
                    size_index = name_list[index].index(column)
                    write += str(size_list[index][size_index])
                else:
                    write += '0'
            
            #commit to file
            write += '\n'
            write_file.write(write)
    

