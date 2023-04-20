def old_PDB_new_pdb(file_name, protein_remain):
    """Generates a new PDB file with protein information based on a list of remaining protein numbers.

    This function reads a PDB file, extracts protein information for the proteins whose numbers are specified
    in the `protein_remain` list, and writes the extracted information to a new PDB file.

    Args:
        file_name (str): The name of the input PDB file to be read.
        protein_remain (list): A list of protein numbers for which the protein information needs to be extracted.

    Returns:
        int: Returns 0 upon successful generation of the new PDB file.
    """
    with open(file_name, 'r') as file:
        write_lst = []
        for line in file.readlines():
            line_ = line.split(' ')
            if line_[0] == 'TITLE':
                write_lst.append(line)
            elif line_[0] == 'CRYST1':
                write_lst.append(line)
            elif line_[0] == 'ATOM':
                info = []
                for i in line_:
                    i.strip('\n')
                    if i != '':
                        info.append(i)
                info[9] = info[9].strip('\n')
                if int(info[4]) in protein_remain:
                    write_lst.append(line)
    with open('output_file.pdb', 'w') as file_:
        file_.seek(0)
        file_.truncate()
        for i in write_lst:
            file_.writelines(i)
    return 0


