import os
"""Reads in every single file in the library, and allows you to get data about it. Currently gets:
    - Number of lines
    - Number of main functions (this means no functions call them. In theory, meant to be run by user)
    - Number of functions
    - other libraries imported
    - % docstringed!!!!!
"""

def search_folder(dir: str):
    search_folder_no_ret(dir)
    return py_list

def search_folder_no_ret(dir: str):
    """Will take in a directory and find all directories within it.

    Args:
        dir (str): The directory it is searching
    """
    file_list = os.listdir(dir)

    for file in file_list:
        if file.endswith('.py') and not file.startswith("__"):
            py_list.append(f"{dir}\{file}")

        if not '.' in file:
            search_folder_no_ret(f"{dir}\{file}")


if __name__ == "__main__":
    #get names of all files
    dir_start = "ioNERDSSPyPi\ioNERDSS\\functions"
    py_list = []
    py_list = search_folder(dir_start)


    #get var the holds the names of each file
    allFuncNames = []
    mainFunctions = []
    for file in py_list:
        fileName = file.split('\\')[-1]
        allFuncNames.append(fileName)
        mainFunctions.append(fileName[0:-3])
    
    #print(mainFunctions)

    #Create vars that hold the data!
    importSet = set()
    numberOfLines = 0
    docStringCount = 0
    needsDoc = []

    #run through each py file
    for file in py_list:
        with open(f"{file}",mode="r") as open_file:

            #gets a list of each line in the file
            lines = open_file.readlines()
            docString = False

            #reads through each line
            for line in lines:

                #gets import
                if line.startswith('import'):
                    check_line = line.split(' ')
                    if '\n' in check_line[1]:
                        check_line[1] = check_line[1][0:-1]
                    importSet.add(check_line[1])

                #sees what files are being imported. If they are they are removed from main function list
                elif line.startswith('from .'):
                    check_line = line.split(' ')
                    func_name = check_line[3][0:-1]
                    if func_name in mainFunctions:
                        mainFunctions.remove(func_name)
                
                #checks if there is a docstring in this line. If there is set this files 'docstring' var to true.
                if "\"\"\"" in line or "'''" in line:
                    docString = True
                
                #gets the number of lienes
                numberOfLines += 1
            
            #if there was at least one """/''' in this file, docstring number goes up. If no tho :///, it gets added to the LIST
            if docString: docStringCount = docStringCount + 1
            else: needsDoc.append(file.split('\\')[-1])                


    mainFunctions.sort()
    print(f"Imports: {importSet}\nNumber of Lines: {numberOfLines}\nNumber of Main Functions: {len(mainFunctions)}\
          \nNumber of Functions: {len(allFuncNames)}\nNumber of Subfunctions: {len(allFuncNames)-len(mainFunctions)}\
          \n% of Files Docstringed: {round(docStringCount/len(allFuncNames),2)*100}%")
    print(f'Needs Docstring: {needsDoc}')
#\nNeeds Docstring: {needsDoc}





