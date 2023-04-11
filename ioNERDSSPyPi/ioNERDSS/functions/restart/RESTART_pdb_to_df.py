import pandas as pd

def RESTART_pdb_to_df(file_name_pdb):
    """Convert protein information from PDB file to a Pandas DataFrame.

    Args:
        file_name_pdb (str): the name of the PDB file to be read.

    Returns:
        df (pd.DataFrame): a DataFrame containing protein information with columns 'Protein_Num' and 'Protein_Name'.

    Examples:
        >>> RESTART_pdb_to_df('protein.pdb')
        DataFrame with protein information:
        Protein_Num Protein_Name
        0            1           PROA
        1            2           PROB
        2            3           PROC
    ...
    """
    df = pd.DataFrame(columns=['Protein_Num', 'Protein_Name'])
    with open(file_name_pdb, 'r') as file:
        index = 0
        for line in file.readlines():
            line = line.split(' ')
            if line[0] == 'ATOM':
                info = []
                for i in line:
                    if i != '':
                        info.append(i)
                df.loc[index, 'Protein_Num'] = int(info[4])
                df.loc[index, 'Protein_Name'] = info[3]
            index += 1
        df = df.dropna()
        df = df.reset_index(drop=True)
    return df


