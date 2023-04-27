import numpy as np


def multi_hist_to_csv(FileName: str):
    """Creates a .csv (spreadsheet) file from a histogram.dat file (multi-species)

    Args:
        FileName (str): Path to the histogram.dat file

    Returns:
        histogram.csv file: Each row is a different time stamp (all times listed in column A). Each column is a different size of complex molecule (all sizes listed in row 1). Each box 
        is the number of that complex molecule at that time stamp.
    """
    
    column_list = [] #holds the name of each column (Time + each complex name)
    time_list = [] #holds each time. Index corresponds to a sublist in name_count_dict_List
    name_count_dict_list = [] #holds each name/count. Index corresponds with size_list

    name_count_dict_sub = {} #holds dictionary that holds names and counts. Appends to name_count_dict_list

    #Creates list with every complex type/size
    with open(FileName, 'r') as file:
        for index,line in enumerate(file.readlines()):
            
            #if it is a time stamp
            if line[0:9] == 'Time (s):':
                time = float(line.split(' ')[-1])
                time_list.append(time)

                #if there was a previous timestamp before it that needs to be initilized
                if index != 0:
                    name_count_dict_list.append(name_count_dict_sub)
                    name_count_dict_sub = {}

            else:
                
                #get name of species & get number of species in this complex
                name = line.split('	')[1].strip(' \n')
                count = int(line.split('\t')[0])
                name_count_dict_sub[name] = count
                #input(f"Time: {time} \n Name: {name} \n Count: {count}")

                #creates a list of every 'name'
                if name not in column_list:
                    column_list.append(name)
    
    #at the end append the final subs because of the fence problem thing :(
    name_count_dict_list.append(name_count_dict_sub)
    name_count_dict_sub = {}
    #input(name_count_dict_list)
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
                if column in name_count_dict_list[index].keys():
                    write += str(name_count_dict_list[index][column])
                else:
                    write += '0'
            
            #commit to file
            write += '\n'
            write_file.write(write)
    
    
    
    
    
    """name_list = ['Time (s)']
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:9] != 'Time (s):':
                name = line.split('	')[1].strip(' \n')
                if name not in name_list:
                    name_list.append(name)
    file.close()
    with open(FileName, 'r') as read_file, open('histogram.csv', 'w') as write_file:
        head = ''
        for i in name_list:
            head += i
            if i != name_list[-1]:
                head += ','
            else:
                head += '\n'
        write_file.write(head)
        stat = np.zeros(len(name_list))
        for line in read_file.readlines():
            if line[0:9] == 'Time (s):':
                if line != 'Time (s): 0\n':
                    write_line = ''
                    for i in range(len(stat)):
                        write_line += str(stat[i])
                        if i != len(stat)-1:
                            write_line += ','
                        else:
                            write_line += '\n'
                    write_file.write(write_line)
                stat = np.zeros(len(name_list))
                write_line = ''
                info = float(line.split(' ')[-1])
                stat[0] += info
            else:
                name = line.split('	')[-1].strip(' \n')
                num = float(line.split('	')[0])
                index = name_list.index(name)
                stat[index] += num
        for i in range(len(stat)):
            write_line += str(stat[i])
            if i != len(stat)-1:
                write_line += ','
            else:
                write_line += '\n'
        write_file.write(write_line)
    read_file.close()
    write_file.close()
    return 0"""


