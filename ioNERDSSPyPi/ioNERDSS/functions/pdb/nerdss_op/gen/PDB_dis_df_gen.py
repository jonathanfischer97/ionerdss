import pandas as pd
from .PDB_dis_cal import PDB_dis_cal


def PDB_dis_df_gen(df, info):
    dis_df = pd.DataFrame(columns=['Protein_Num_1', 'Protein_Name_1', 'Cite_Name_1',
                          'Protein_Num_2', 'Protein_Name_2', 'Cite_Name_2', 'sigma', 'dis'])
    """Generates a distance dataframe for protein-protein interactions based on given information.

    Args:
       df (pd.DataFrame): the input dataframe containing protein information
        info (pd.DataFrame): the input dataframe containing interaction information

    Returns:
        pd.DataFrame: the generated distance dataframe containing calculated distances between protein pairs

    Example:
        >>> df = pd.read_csv('protein_data.csv')
        >>> info = pd.read_csv('interaction_info.csv')
        >>> dis_df = PDB_dis_df_gen(df, info)
        >>> dis_df.head()
        Protein_Num_1 Protein_Name_1 Cite_Name_1 Protein_Num_2 Protein_Name_2 Cite_Name_2 sigma       dis
        0             1          Protein_A       Cite_A             2          Protein_B       Cite_B  2.75  5.196152
        1             1          Protein_A       Cite_A             3          Protein_C       Cite_C  1.25  3.162278
        ...
    """
    index = 0
    count = 1
    for i in range(len(info)):
        df_temp_1 = df[df['Protein_Name'].isin([info.iloc[i, 0]])]
        df_1 = df_temp_1[df_temp_1['Cite_Name'].isin([info.iloc[i, 1]])]
        df_temp_2 = df[df['Protein_Name'].isin([info.iloc[i, 2]])]
        df_2 = df_temp_2[df_temp_2['Cite_Name'].isin([info.iloc[i, 3]])]
        df_1 = df_1.reset_index(drop=True)
        df_2 = df_2.reset_index(drop=True)
        print('Calculating distance for reaction #', count, '...')
        count += 1
        for j in range(len(df_1)):
            for k in range(len(df_2)):
                dis_df.loc[index, 'Protein_Num_1'] = df_1.loc[j, 'Protein_Num']
                dis_df.loc[index, 'Protein_Name_1'] = df_1.loc[j,
                                                               'Protein_Name']
                dis_df.loc[index, 'Cite_Name_1'] = df_1.loc[j, 'Cite_Name']
                dis_df.loc[index, 'Protein_Num_2'] = df_2.loc[k, 'Protein_Num']
                dis_df.loc[index, 'Protein_Name_2'] = df_2.loc[k,
                                                               'Protein_Name']
                dis_df.loc[index, 'Cite_Name_2'] = df_2.loc[k, 'Cite_Name']
                dis_df.loc[index, 'sigma'] = info.loc[i, 'sigma']
                x = [df_1.loc[j, 'x_coord'], df_1.loc[j,
                                                      'y_coord'], df_1.loc[j, 'z_coord']]
                y = [df_2.loc[k, 'x_coord'], df_2.loc[k,
                                                      'y_coord'], df_2.loc[k, 'z_coord']]
                dis_df.loc[index, 'dis'] = PDB_dis_cal(x, y)
                index += 1
    return dis_df


