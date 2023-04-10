import pandas as pd


def PDB_bind_df_gen(dis_df, buffer_ratio):
    """ Generates a new DataFrame containing binding information from a distance DataFrame, based on a buffer ratio.

    Args:
        dis_df (pd.DataFrame): the input distance DataFrame, containing columns 'Protein_Num_1', 'Protein_Name_1',
                                'Cite_Name_1', 'Protein_Num_2', 'Protein_Name_2', 'Cite_Name_2', 'sigma', and 'dis'
        buffer_ratio (float): the buffer ratio used to determine binding, defined as a fraction of 'sigma'

    Returns:
        pd.DataFrame: the generated binding DataFrame, containing the same columns as the input DataFrame

    Raises:
        TypeError: if the input arguments are not of the expected type

    Example:
        >>> dis_df = pd.DataFrame({'Protein_Num_1': [1, 2, 3], 'Protein_Name_1': ['A', 'B', 'C'],
        ...                        'Cite_Name_1': ['X', 'Y', 'Z'], 'Protein_Num_2': [4, 5, 6],
        ...                        'Protein_Name_2': ['D', 'E', 'F'], 'Cite_Name_2': ['M', 'N', 'O'],
        ...                        'sigma': [0.1, 0.2, 0.3], 'dis': [0.05, 0.15, 0.25]})
        >>> buffer_ratio = 0.1
        >>> PDB_bind_df_gen(dis_df, buffer_ratio)
        Protein_Num_1 Protein_Name_1 Cite_Name_1  Protein_Num_2 Protein_Name_2 Cite_Name_2  sigma   dis
        0             1              A           X             4              D          M    0.1  0.05
        1             2              B           Y             5              E          N    0.2  0.15
    """
    bind_df = pd.DataFrame(columns=['Protein_Num_1', 'Protein_Name_1', 'Cite_Name_1',
                           'Protein_Num_2', 'Protein_Name_2', 'Cite_Name_2', 'sigma', 'dis'])
    index = 0
    for i in range(len(dis_df)):
        if dis_df.loc[i, 'dis'] >= dis_df.loc[i, 'sigma']*(1-buffer_ratio):
            if dis_df.loc[i, 'dis'] <= dis_df.loc[i, 'sigma']*(1+buffer_ratio):
                bind_df.loc[index] = dis_df.loc[i]
                index += 1
    return bind_df


