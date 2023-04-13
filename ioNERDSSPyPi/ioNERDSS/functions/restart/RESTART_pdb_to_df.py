
def RESTART_pdb_to_df(file_name_pdb):
    """Convert protein information from PDB file to a dictionary

    Args:
        file_name_pdb (str): the name of the PDB file to be read.

    Returns:
        dictionary: a dictionary with key = number, value = protein type
    Examples:
        >>> RESTART_pdb_to_df_alt('protein.pdb')
        {1: 'clat',2: 'clat',3:'dode',....}
    ...
    """
    pdb_dict = {}
    with open(file_name_pdb, 'r') as file:

        for line in file.readlines():
            line = line.split(' ')
            if line[0] == 'ATOM':
                info = []
                for i in line:
                    if i != '':
                        info.append(i)
                pdb_dict[int(info[4])] = info[3]

    return pdb_dict


