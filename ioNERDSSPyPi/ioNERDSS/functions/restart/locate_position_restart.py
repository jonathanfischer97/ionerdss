from .RESTART_read_restart import RESTART_read_restart
from .RESTART_pdb_to_df import RESTART_pdb_to_df
from .RESTART_complex_df_gen import RESTART_complex_df_gen
from .RESTART_find_complex_df import RESTART_find_complex_df
from .RESTART_new_pdb import RESTART_new_pdb


def locate_position_restart(FileNamePdb, NumList, FileNameRestart='restart.dat'):
    """
    Locates specific complexes of a certain size from a PDB file along with 'restart.dat' file after simulation and outputs the result
    as a separated file named "output_file.pdb" containing only the desired complex.

    Args:
        FileNamePdb (str): The path to the PDB file, which is usually the last frame of simulation.
        NumList (List[int]): A list of integers representing the number of individual monomers in the complex that the user
            needs to locate, and the order of the monomers in the list is determined by the order in which they appear in the PDB file.
        FileNameRestart (str, optional): The path to the 'restart.dat' file. Defaults to 'restart.dat'.

    Returns:
        output_file.pdb: seperate file containing only the desired complex(es)
    
    Note:
        The advantage of reading the 'restart.dat' file is that the file directly stores the binding information of each complex
        in the system and can be used directly, so the function runs faster; however, the function is not universal, if the
        'restart.dat ' file's write logic changes, then this function will no longer work.

    Raises:
        FileNotFoundError: If the specified PDB file or 'restart.dat' file cannot be found.
        TypeError: If the specified NumList is not a list of integers.

    Examples:
        >>> locate_position_restart('/Users/UserName/Documents/999999.pdb', [12], '/Users/UserName/Documents/restart.dat')
        "/Users/UserName/Documents/output_file.pdb"
    """

    print('Reading restart.dat......')
    complex_lst = RESTART_read_restart(FileNameRestart)
    print('Reading files complete!')

    print('Reading PDB files......')
    pdb_df = RESTART_pdb_to_df(FileNamePdb)
    print('Reading files complete!')

    print('Finding complexes......')
    complex_df = RESTART_complex_df_gen(pdb_df, complex_lst)
    print('Finding complexes complete!')

    print('Writing new PDB files......')
    protein_remain = RESTART_find_complex_df(complex_df, NumList, pdb_df)
    RESTART_new_pdb(FileNamePdb, protein_remain)
    print('PDB writing complete!(named as output_file.pdb)')
    
    return 0


