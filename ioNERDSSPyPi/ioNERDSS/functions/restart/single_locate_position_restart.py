from .read_restart import read_restart
from .write_pdb import write_pdb


def single_locate_position_restart(FileNamePdb, ComplexSize, FileNameRestart='restart.dat'):
    """ Reads a restart.dat file and a PDB file, identifies protein complexes of a certain size, creates a new PDB file
    containing only the proteins corresponding to those complexes, and writes the new PDB file.

    Args:
        FileNamePdb (str): the name of the input PDB file
        ComplexSize (int): the size of protein complexes to be located
        FileNameRestart (str, optional): the name of the input restart.dat file (default is 'restart.dat')

    Returns:
        output_file.pdb: holds all of the proteins that were in a complex of a certain size

    """

    print('Reading restart.dat...')
    complex_lst = read_restart(FileNameRestart)
    print('Reading files complete!')
    protein_remain = []
    for i in complex_lst:
        if len(i) == ComplexSize:
            print(i)
            print(len(i))
            protein_remain.append(i)
    protein_remain_flat = []
    for i in protein_remain:
        for j in i:
            protein_remain_flat.append(j)
    write_pdb(FileNamePdb, protein_remain_flat)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0