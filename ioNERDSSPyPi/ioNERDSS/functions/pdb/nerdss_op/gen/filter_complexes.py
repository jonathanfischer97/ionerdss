
def filter_complexes(complex_lst,num_name_dict,num_dict):
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

    complex_filtered = []
    #run through every protein complex
    for complex in complex_lst:
        temp_complex_num = {}
        for value in set(list(num_name_dict.values())):
            temp_complex_num[value] = 0
        #for each protein
        for protein in complex:
            temp_complex_num[num_name_dict[str(protein)]] = temp_complex_num[num_name_dict[str(protein)]] + 1

        
        if temp_complex_num == num_dict:
            for protein in complex:
                complex_filtered.append(protein)


    return complex_filtered

   