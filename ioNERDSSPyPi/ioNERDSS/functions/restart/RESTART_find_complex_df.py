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
    
    #each row of the dataframe
    for row in list_of_rows:

        #if row/protein complex has the correct number of each protein type
        if row[0:-1] == num_lst: 
            
            protein_complex_hits += 1
            list_of_protein_nums = row[-1].strip('[').strip(']').split(',') #gets the list of the specific proteins in this complex
            
            #add every protein num that is in that complex
            for protein_num in list_of_protein_nums:
                protein_remain.append(int(protein_num))
    
    #print success / failure
    if protein_complex_hits == 0:
        print('No complexes where found with the specific number of protein types.')
    else:
        print(f'Found {protein_complex_hits} protein complexes!')

    return protein_remain


