def PDB_find_complex(pdb_df, bond_lst):
    """Finds protein complexes based on a list of protein-protein bond pairs.

    Args:
        pdb_df (DataFrame): A pandas DataFrame containing information about proteins.
        bond_lst (list): A list of protein-protein bond pairs in the format [protein_num_1, protein_num_2].

    Returns:
        list: A list of protein complex lists, where each complex list contains protein numbers that are part of
        the same complex.

    Example:
        Given a protein DataFrame `pdb_df` with the following structure:

        | Protein_Name | Protein_Num |
        |--------------|-------------|
        | Protein A    | 1           |
        | Protein B    | 2           |
        | Protein C    | 3           |
        | Protein D    | 4           |
        | Protein E    | 5           |

        And a `bond_lst` of [[1, 2], [2, 3], [4, 5]], the function will return the following list of protein
        complexes:

        [[1, 2, 3], [4, 5]].
    """

    complex_lst = []
    for i in range(1, 1+pdb_df['Protein_Num'].max()):
        complex_temp = [i]
        j = 0
        while j < len(bond_lst):
            if bond_lst[j][0] in complex_temp and bond_lst[j][1] not in complex_temp:
                complex_temp.append(bond_lst[j][1])
                j = 0
            elif bond_lst[j][1] in complex_temp and bond_lst[j][0] not in complex_temp:
                complex_temp.append(bond_lst[j][0])
                j = 0
            else:
                j += 1
        complex_lst.append(complex_temp)
    for i in complex_lst:
        i.sort()
    complex_lst_ = []
    for i in complex_lst:
        if i not in complex_lst_:
            complex_lst_.append(i)
    return complex_lst_


