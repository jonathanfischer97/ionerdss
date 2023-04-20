import pandas as pd


def old_PDB_complex_df_gen(pdb_df, complex_lst):
    """Generates a DataFrame containing complex information from a given DataFrame and a list of complexes.

    Args:
        pdb_df (pd.DataFrame): the input DataFrame containing protein information
        complex_lst (List[List[str]]): a list of complexes, where each complex is represented as a list of protein names

    Returns:
        pd.DataFrame: the generated complex information DataFrame, with columns corresponding to unique protein names
                    in the input DataFrame, and an additional column 'Protein_Num' representing the total number of proteins
                    in each complex

    Raises:
        ypeError: if pdb_df is not a pandas DataFrame or complex_lst is not a list of lists

    Example:
        >>> pdb_df = pd.DataFrame({'Protein_Name': ['A', 'B', 'C'],
                                'Protein_Num': [1, 2, 3]})
        >>> complex_lst = [['A', 'B'], ['B', 'C'], ['A', 'C']]
        >>> PDB_complex_df_gen(pdb_df, complex_lst)
        A  B  C  Protein_Num
        0  1  1  0             2
        1  0  1  1             2
        2  1  0  1             2
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


