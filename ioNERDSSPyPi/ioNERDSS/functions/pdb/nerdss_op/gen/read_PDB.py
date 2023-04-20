import pandas as pd

def read_PDB(file_name, drop_COM):
    """Converts a PDB file to a Pandas DataFrame.

    Args:
        file_name (str): Name of the PDB file to be read.
        drop_COM (bool): Whether to drop lines with 'COM' as the 'Cite_Name' value.

    Returns:
        numpy array: array that stores all of the proteins info
            - [i] = each row, different protein site
            - [i][i] = each column (in a specific row) find the index of the correct colum with the dictionary
                - Ex: site_dict['Protein_Num'] >> 0
        dictionary: dictionary that stores the index of each column    
    
    """

    site_array = []
    site_dict = {'Protein_Num':0,'Protein_Name':1,'Site_Name':2,'x_coord':3,'y_coord':4,'z_coord':5}
    num_name_dict = {}

    with open(file_name, 'r') as file:
        
        for line in file.readlines():
            line = line.split(' ')
            
            #if the line discribes a site, take info from it and put it into site_array
            if line[0] == 'ATOM':
                    info = []
                    info = [element for element in line if element !=""] #removes white space from line
                    
                    if (drop_COM and info[2] != 'COM') or not drop_COM:

                        site_array.append([])
                        index = len(site_array) - 1

                        site_array[index].append(int(info[4]))
                        site_array[index].append(info[3])
                        site_array[index].append(info[2])
                        site_array[index].append(float(info[5]))
                        site_array[index].append(float(info[6]))
                        site_array[index].append(float(info[7]))

                        num_name_dict[info[4]] = info[3]

                        

    return site_array,site_dict,num_name_dict


