def old_PDB_find_complex_df(complex_df, num_lst, pdb_df):
    """Finds remaining proteins in a complex DataFrame based on a given list of protein numbers.

    Args:
        complex_df (DataFrame): A pandas DataFrame containing information about protein complexes.
        num_lst (list): A list of protein numbers to search for in the complex DataFrame.
        pdb_df (DataFrame): A pandas DataFrame containing information about proteins.

    Returns:
        list: A list of protein numbers that remain in the complex DataFrame after filtering based on the given
        list of protein numbers.

    Example:
        Given a complex DataFrame with the following structure:

        | Protein_Num | Num_List              |
        |-------------|-----------------------|
        | Complex 1   | [1, 2, 3]             |
        | Complex 2   | [1, 3, 4, 5]          |
        | Complex 3   | [2, 4, 5]             |

        And a protein DataFrame `pdb_df` with the following structure:

        | Protein_Name | Protein_Num |
        |--------------|-------------|
        | Protein A    | 1           |
        | Protein B    | 2           |
        | Protein C    | 3           |
        | Protein D    | 4           |
        | Protein E    | 5           |

        And a `num_lst` of [1, 3], the function will return the following list of remaining protein numbers:
        [2].
    """
    
    protein_name = []
    for i in range(len(pdb_df)):
        if pdb_df.loc[i, 'Protein_Name'] not in protein_name:
            protein_name.append(pdb_df.loc[i, 'Protein_Name'])
    complex_df['Num_List'] = ''
    for i in range(complex_df.shape[0]):
        lst = []
        for j in range(complex_df.shape[1]-2):
            lst.append(complex_df.iloc[i, j])
        complex_df.loc[i, 'Num_List'] = str(lst)
    num_lst_str = str(num_lst)
    protein_remain = []
    for i in range(complex_df.shape[0]):
        if complex_df.loc[i, 'Num_List'] == num_lst_str:
            string = complex_df.loc[i, 'Protein_Num']
            string = string.strip('[').strip(']').split(',')
            for i in string:
                protein_remain.append(int(i))
    return protein_remain


