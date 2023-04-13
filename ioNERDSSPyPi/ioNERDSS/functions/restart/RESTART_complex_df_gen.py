import pandas as pd


def RESTART_complex_df_gen(pdb_dict, complex_lst):
    """Generates a dataframe that represents the complexes from a given pdb dataframe and complex list.

    Args:
        pdb_df (pandas.DataFrame): DataFrame containing the PDB data with columns ['Protein_Num', 'Protein_Name'].
        complex_lst (list): List of lists containing the protein numbers that form each complex.

    Returns:
        pandas.DataFrame: A DataFrame where each row represents a complex and each column represents a protein. 
        The values of the DataFrame correspond to the number of atoms of each protein in each complex.
        set: has a list of each unique protein name
    """

    #create a list of each unique protein name in the dataframe
    protein_name_set = set(list(pdb_dict.values()))
    
    #Creates new dataframe with each unique protein as a differen column
    column_lst = [] # a list of the columns in the df
    for i in protein_name_set:
        column_lst.append(i)
    column_lst.append('Protein_Num')
    complex_df = pd.DataFrame(columns=column_lst) # Dataframe with columns = protein types. Rows = protein complex.

    for index,protein_complex in enumerate(complex_lst):
        #runs as every different protein complex

        #Creates a new row for each protein complex and adds the protein numbers into the 'protein num' column
        complex_df.loc[index] = 0
        complex_df.loc[index, 'Protein_Num'] = str(protein_complex)

        #will find the number of each protein type in each complex then add it to the new dataframe.
        for protein in protein_complex:
            #for each protein (number) in this complex

            #get the proteins type from the dictionary
            protein_type = pdb_dict[protein]

            #adds 1 to this protein's type for this protein complex
            complex_df.loc[index, protein_type] += 1
    return complex_df



