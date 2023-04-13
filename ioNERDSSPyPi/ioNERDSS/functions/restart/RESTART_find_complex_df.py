def RESTART_find_complex_df(complex_df, num_lst):
    """Finds the complexes with the correct number of proteins of each type.
    
    Args:
        complex_df: A pandas DataFrame that contains information about the complexes, including the protein numbers 
                    that form the complex.
        num_lst: A list of integers representing the protein numbers of the proteins to be found in the complex.
        pdb_dict: A dictionary with keys: protein number, values: protein type
    
    Returns:
        A list of integers representing the protein numbers that form the given complex.
    """


    list_of_rows = complex_df.loc[0:].values.tolist()
    protein_remain = [] #list of proteins in the complexes (what is returned)
    protein_complex_hits = 0 #how many protein complexes have the correct number
    

    #run through each row of the dataframe
    for row in list_of_rows:
        #for every row/complex_protein in the dataframe

        if row[0:-1] == num_lst: 
            #if row/complex_protein has the correct number of proteins in each structure
            protein_complex_hits += 1

            list_of_protein_nums = row[-1].strip('[').strip(']').split(',') #this is a list of the proteins in this complex
            for protein_num in list_of_protein_nums:
                #add every protein num that is in that complex
                protein_remain.append(int(protein_num))
    
    
    if protein_complex_hits == 0:
        print('No complexes where found with the specific number of protein types.')
    else:
        print(f'Found {protein_complex_hits} protein complexes!')

    return protein_remain

"""#creates a new column in complex_df that stores a list of the number of each protein type in that complex
    complex_df['Num_List'] = '' #adds num_list column to df
    for row in range(complex_df.shape[0]):
        #for each row in the dataframe

        lst = []
        for column in range(complex_df.shape[1]-2):
            #for each column in this row (not including protein_num,num_list)

            lst.append(complex_df.iloc[row, column])

        complex_df.loc[row, 'Num_List'] = str(lst)
    input(f'{complex_df}')

    #finds proteins that have a size equal to inputted number
    protein_remain = [] #list of proteins with size = input number
    for row in range(complex_df.shape[0]):
        #for each row

        input(f"{complex_df.loc[row, 'Num_List']} == {str(num_lst)}")
        if complex_df.loc[row, 'Num_List'] == str(num_lst):
            #if that rows num_list = inputted

            protein_list = complex_df.loc[row, 'Protein_Num']
            protein_list = protein_list.strip('[').strip(']').split(',')
            for protein in protein_list:
                protein_remain.append(int(protein))
            input(f"{protein_remain}")
    return protein_remain"""


