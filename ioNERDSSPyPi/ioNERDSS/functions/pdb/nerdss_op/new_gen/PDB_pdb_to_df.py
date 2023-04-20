import pandas as pd

def old_PDB_pdb_to_df(file_name, drop_COM):
    """Converts a PDB file to a Pandas DataFrame.

    Args:
        file_name (str): Name of the PDB file to be read.
        drop_COM (bool): Whether to drop lines with 'COM' as the 'Cite_Name' value.

    Returns:
        pd.DataFrame: A DataFrame containing the protein information extracted from the PDB file.
            The DataFrame has the following columns:
            - 'Protein_Num': Protein number (integer).
            - 'Protein_Name': Protein name (string).
            - 'Cite_Name': Cite name (string).
            - 'x_coord': x-coordinate of the protein (float).
            - 'y_coord': y-coordinate of the protein (float).
            - 'z_coord': z-coordinate of the protein (float).
    """
    df = pd.DataFrame(columns=['Protein_Num', 'Protein_Name',
                      'Cite_Name', 'x_coord', 'y_coord', 'z_coord'])
    
    with open(file_name, 'r') as file:
        
        for index,line in enumerate(file.readlines()):
            line = line.split(' ')
            if line[0] == 'ATOM':
                info = []
                for i in line:
                    if i != '':
                        info.append(i)
                df.loc[index, 'Protein_Num'] = int(info[4])
                df.loc[index, 'Protein_Name'] = info[3]
                df.loc[index, 'Cite_Name'] = info[2]
                df.loc[index, 'x_coord'] = float(info[5])
                df.loc[index, 'y_coord'] = float(info[6])
                df.loc[index, 'z_coord'] = float(info[7])
        df = df.dropna()
        if drop_COM:
            df = df.drop(index=df[(df.Cite_Name == 'COM')].index.tolist())
        df = df.reset_index(drop=True)
    return df


