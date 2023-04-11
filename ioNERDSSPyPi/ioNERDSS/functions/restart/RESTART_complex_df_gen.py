import pandas as pd


def RESTART_complex_df_gen(pdb_df, complex_lst):
    """Generates a dataframe that represents the complexes from a given pdb dataframe and complex list.

    Args:
        pdb_df (pandas.DataFrame): DataFrame containing the PDB data with columns ['Protein_Num', 'Protein_Name'].
        complex_lst (list): List of lists containing the protein numbers that form each complex.

    Returns:
        pandas.DataFrame: A DataFrame where each row represents a complex and each column represents a protein. 
        The values of the DataFrame correspond to the number of atoms of each protein in each complex.
    """

    name_lst = list(pdb_df['Protein_Name'])
    name_lst_ = []
    for i in name_lst:
        if i not in name_lst_:
            name_lst_.append(i)
    column_lst = []
    for i in name_lst_:
        column_lst.append(i)
    column_lst.append('Protein_Num')
    complex_df = pd.DataFrame(columns=column_lst)
    index = 0
    for i in complex_lst:
        complex_df.loc[index] = 0
        complex_df.loc[index, 'Protein_Num'] = str(i)
        for j in i:
            for indexs in pdb_df.index:
                for k in range(len(pdb_df.loc[indexs].values)):
                    if(pdb_df.loc[indexs].values[k] == j):
                        col = pdb_df.loc[indexs, 'Protein_Name']
                        complex_df.loc[index, col] += 1
                        break
                else:
                    continue
                break
        index += 1
    return complex_df


