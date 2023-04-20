from .gen.PDB_pdb_to_df import old_PDB_pdb_to_df
from .gen.PDB_dis_df_gen import old_PDB_dis_df_gen
from .gen.PDB_bind_df_gen import old_PDB_bind_df_gen
from .gen.PDB_find_bond import old_PDB_find_bond
from .gen.PDB_find_complex import old_PDB_find_complex
from .gen.PDB_complex_df_gen import old_PDB_complex_df_gen
from .gen.PDB_find_complex_df import old_PDB_find_complex_df
from .gen.PDB_new_pdb import old_PDB_new_pdb
from .gen.PDB_binding_info_df import old_PDB_binding_info_df


def locate_position_PDB(FileNamePdb, NumList, FileNameInp, BufferRatio=0.01):
    """
    Locates specific complexes of a certain size from a PDB file after simulation and outputs the result as a separated file
    named "output_file.pdb" containing only the desired complex.

    Args:
        FileNamePdb (str): The path to the PDB file, which is usually the last frame of the simulation.
        NumList (List[int]): A list of integers representing the number of individual monomers in the complex that the user
            needs to locate, and the order of the monomers in the list is determined by the order in which they appear in the PDB file.
        FileNameInp (str): The path to the '.inp' file, which usually stores the reaction information.
        BufferRatio (float, optional): The buffer ratio used to determine whether two reaction interfaces can be considered as bonded.
            Defaults to 0.01.

    Returns:
        output_file.pdb: A file containing the desired complex.

    Note:
        Reading only the PDB file slows down the function compared to reading the 'restart.dat' file, because the function needs
        to calculate the distance between all reactive atoms that can be reacted based on the reaction information to determine
        whether they are bound or not. Therefore, this function is universal but runs slowly in time.
    
    Raises:
        FileNotFoundError: If the specified PDB file or '.inp' file cannot be found.
        TypeError: If the specified NumList is not a list of integers.

    Examples:
        >>> locate_position_PDB('/Users/UserName/Documents/999999.pdb', [12], '/Users/UserName/Documents/parms.inp', 0.05)
        "/Users/UserName/Documents/output_file.pdb"
    """

    #reads in the .pdb file
    print('Reading files......')
    pdb_df = old_PDB_pdb_to_df(FileNamePdb, True)
    print('Reading files complete!')

    print('Extracting binding information......')
    binding_info = old_PDB_binding_info_df(FileNameInp)
    print('Extracting complete!')

    print('Calculating distance......')
    dis_df = old_PDB_dis_df_gen(pdb_df, binding_info)
    print('Calculation complete!')

    print('Finding bonds......')
    bind_df = old_PDB_bind_df_gen(dis_df, BufferRatio)
    bond_lst = old_PDB_find_bond(bind_df)
    print('Finding bonds complete!')

    print('Finding complexes......')
    complex_lst = old_PDB_find_complex(pdb_df, bond_lst)
    complex_df = old_PDB_complex_df_gen(pdb_df, complex_lst)
    print('Finding complexes complete!')
    
    print('Writing new PDB files......')
    protein_remain = old_PDB_find_complex_df(complex_df, NumList, pdb_df)
    old_PDB_new_pdb(FileNamePdb, protein_remain)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0


