import os
import numpy as np



def save_vars_to_file(var_dict: dict):



    #create folder if necessary 
    file_start = "" #the starting part of the file

    #if there is a folder needed
    if len(var_dict) > 1:
        file_start = "vars/"

        #if the folder needs to be made
        if not os.path.exists("vars"):
            os.mkdir(path="vars")


    for key,value in var_dict.items():

        type = "" # what kind of file is being made
        file_end = "" # the ending part of the file
    
        #determine variable type
        if isinstance(value,int) or isinstance(value,float): #number
            file_end = f"{key}_number.txt"
            type = "txt"
        elif isinstance(value,str): #string
            file_end = f"{key}_string.txt"
            type = "txt"    
        elif isinstance(value,list) or isinstance(value,np.ndarray): #list
            
            #if empty lists, add a zero
            if value == []:
                value.append("EMPTY LIST")

            file_end = f"{key}_list.csv"
            if isinstance(value[0],list) or isinstance(value[0],np.ndarray): #2dim+ deep list
                type = "2list" 
            else: #1dim list
                type = "1list"
        else:
            file_end = f"{key}_na.txt"
            type = "txt"
        
        file_name = file_start + file_end


        #Create file name and open file 
        with open(file_name, mode = "w") as file:

            #if it is just basic text
            if type == "txt":
                file.write(str(value))
            
            #if it is a 1dim list
            elif type == "1list":
                file.write(str(value[0]))
                for var in value:
                    file.write(f",{var}")
            
            #if it is a 2dem list
            elif type == "2list":

                #run through each sub list
                for index,list1 in enumerate(value):
                    
                    #add \n, unless it is the first sublist
                    if index != 0:
                        file.write("\n")
                    
                    #write in entire sublist
                    file.write(f"{list1[0]}")
                    for list2 in list1:
                        file.write(f",{list2}")




            

        




