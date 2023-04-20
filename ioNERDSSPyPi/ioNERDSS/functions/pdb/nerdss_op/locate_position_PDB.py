from .gen.read_PDB import read_PDB
from .gen.read_inp import read_inp
from .gen.create_bond_list import create_bond_list
from .gen.create_complex_list import create_complex_list
from .gen.filter_complexes import filter_complexes
from .gen.write_new_PDB import write_new_PDB


def locate_position_PDB(FileNamePdb, NumDict, FileNameInp, BufferRatio=0.01):
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
    site_array,site_dict,num_name_dict = read_PDB(FileNamePdb, True)
    print('Reading files complete!')

    #reads in the .inp file
    print('Extracting binding information......')
    binding_array,binding_dict = read_inp(FileNameInp)
    print('Extracting complete!')

    #creates list of every bond
    print('Calculating distance......')
    bonds_lst= create_bond_list(site_array,site_dict,binding_array,binding_dict,BufferRatio)
    print('Calculation complete!')

    #creates list of each complex
    print('Finding complexes......')
    complex_lst = create_complex_list(bonds_lst)
    print('Finding complexes complete!')

    #creates list of each complex that has the correct number of each type
    print('Filtering complexes......')
    complex_filtered = filter_complexes(complex_lst,num_name_dict,NumDict)
    print('Filtering complexes complete!')

    #protein_remain = PDB_find_complex_df(complex_lst, NumList, site_array,site_dict)
    print('Writing new PDB files......')
    write_new_PDB(FileNamePdb, complex_filtered)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0


