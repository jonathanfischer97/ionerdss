def PDB_find_bond(bind_df):
    """Finds unique protein bond pairs from a binding DataFrame.

    Args:
        bind_df (DataFrame): A pandas DataFrame containing information about protein bond pairs.

    Returns:
        list: A list of unique protein bond pairs, where each bond is represented as a list of two integers,
        corresponding to the protein numbers of the interacting proteins.

    Example:
        Given a binding DataFrame with the following structure:

        | Protein_Num_1 | Protein_Num_2 |
        |---------------|---------------|
        | 1             | 2             |
        | 2             | 3             |
        | 1             | 3             |
        | 4             | 5             |

        The function will return the following list of unique protein bond pairs:
        [[1, 2], [1, 3], [2, 3], [4, 5]].
    """
    
    bond_lst = []
    for i in range(len(bind_df)):
        bond_lst.append([int(bind_df.loc[i, 'Protein_Num_1']),
                        int(bind_df.loc[i, 'Protein_Num_2'])])
    for i in bond_lst:
        i.sort()
    bond_lst_ = []
    for i in bond_lst:
        if i not in bond_lst_:
            bond_lst_.append(i)
    return bond_lst_


