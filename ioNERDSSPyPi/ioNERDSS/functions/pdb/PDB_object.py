
class ProteinComplex():
    """This object contains all the functions (as methods) necessary to edit a protein complex input using a .pdb file. Then once you are done editing, it can output it as 
    as NERDSS input, a new .pdb file, or a 3D graph of the complex.
    """


    def __init__(self,FileName: str,ChainsIncluded: list = [None]):
        """Initilizes the ProteinComplex object by reading off of a .pdb file

        Args:
            Filename (str): The full path of the desired PDB file or name of the file if in same directory. 
            ChainsIncluded (list, optional): A list of which chains you want to be included. MUST BE MORE THAN 2!
        """
        from . import real_PDB_separate_read

        if len(ChainsIncluded) >= 2 or ChainsIncluded == [None]:
            self.reaction_chain, self.int_site, self.int_site_distance, self.unique_chain, self.COM = real_PDB_separate_read(FileName,ChainsIncluded)
        else:
            raise Exception('The ChainsIncluded list, if included, must be greater then 2')


    ## EDITS DATA ##

    def calc_angle(self):
        """This function calculates the 5 associating angles of each pair of interfaces.
        The default normal vector will be assigned as (0, 0, 1). If the co-linear issue occurs, 
        the system will use (0, 1, 0) instead to resolve co-linear issue. The calculated 5 angles 
        will be shown on the screen automatically."""
        from . import real_PDB_separate_angle

        op = real_PDB_separate_angle((self.reaction_chain, self.int_site, self.int_site_distance, 
                                      self.unique_chain, self.COM))
        self.set_self_from_tuple(op)
    


    def set_COM(self):
        """Normalizes the COM of each chain in the given Result and subtracts the interface coordinates of each chain by their respective COM.
        """
        from . import real_PDB_separate_COM 

        op = real_PDB_separate_COM((self.reaction_chain, self.int_site, self.int_site_distance, 
                                    self.unique_chain, self.COM, self.angle, self.normal_point_lst1, 
                                    self.normal_point_lst2, self.one_site_chain))
        self.set_self_from_tuple(op)



    def filter(self,ChainList):
        """This function will filter the desired chain according to the input list of chain and exclude all the 
            unnecessary coordinate information for future analysis.
        Args:
            ChainList (list): The desired name of chains that users intend to examine. 

        """
        from . import real_PDB_separate_filter

        op =  real_PDB_separate_filter((self.reaction_chain, self.int_site, self.int_site_distance, 
                                    self.unique_chain, self.COM),ChainList)

        self.set_self_from_tuple(op)



    def set_sigma(self):
        """This function allows users to change the value of sigma (the distance between two binding interfaces). 
        The new sigma value and the corresponding coordinates of interfaces will be shown on the screen and the 
        returns will contain all the information for further analysis. 

        Args:
            ChangeSigma (bool, optional): If True, the users are capable of changing the sigma value; 
                                        if False, the sigma will remain as the original ones. 
            SiteList (list, optional): It consists of the serial numbers of the pair of interfaces for which 
                                    the user needs to modify the sigma value. The serial number is determined 
                                    by the pairing sequence shown by the function ‘real_PDB_separate_read’. 
                                    The serial number should be no greater than the total number of interface 
                                    pairs and no smaller than 0. If the serial number is 0, it means to change 
                                    all pairs of interfaces into a same sigma value.
            NewSigma (list, optional): It consists of the actual sigma value that users desire to change, according 
                                    to the sequence of input ‘SiteList’. 
        """
        from . import real_PDB_separate_sigma

        op = real_PDB_separate_sigma((self.reaction_chain, self.int_site, self.int_site_distance, 
                                    self.unique_chain, self.COM))
        self.set_self_from_tuple(op)
    

    ## OUTPUTS DATA ##

    def write_new_input(self):
        """Generates a PDB file containing the calculated COMs and reaction interfaces for visualization and comparison with the 
        original PDB file. The input must be the output result of the 'real_PDB_separate_read' function. Note that the unit for 
        the coordinates in the PDB file is Angstrom, not nm, so the values will be 10 times larger than those in NERDSS input 
        files.
        """
        from . import real_PDB_separate_write

        real_PDB_separate_write((self.reaction_chain, self.int_site, self.int_site_distance, 
                                    self.unique_chain, self.COM, self.angle, self.normal_point_lst1, 
                                    self.normal_point_lst2, self.one_site_chain))



    def show_3D_graph(self):
        """Generate a 3D plot to display the spatial geometry of each simplified chain.
        """
        from . import real_PDB_show_3D

        real_PDB_show_3D((self.reaction_chain, self.int_site, self.int_site_distance, 
                                    self.unique_chain, self.COM))
        


    def write_new_PDB(self):
        """Generate a 3D plot to display the spatial geometry of each simplified chain.
        """
        from . import real_PDB_show_PDB

        real_PDB_show_PDB((self.reaction_chain, self.int_site, self.int_site_distance, 
                                    self.unique_chain, self.COM))


    ## GENERAL METHODS ###

    def set_self_from_tuple(self,op: tuple):
        """Will turn outputted tuple into attributes of this object

        Args:
            op (tuple): The output of one of the functions
        """

        print('setting self from tuple')
        if len(op) == 5:
            self.reaction_chain, self.int_site, self.int_site_distance, self.unique_chain, self.COM = op
        elif len(op) == 9:
            self.reaction_chain, self.int_site, self.int_site_distance, self.unique_chain, self.COM, self.angle, self.normal_point_lst1, self.normal_point_lst2, self.one_site_chain = op
        else:
            raise Exception('The tuple must have a length of 5 or 9')


