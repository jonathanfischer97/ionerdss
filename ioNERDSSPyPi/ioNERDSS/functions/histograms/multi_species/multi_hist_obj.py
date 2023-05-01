from .read_multi_hist import read_multi_hist 
from ..line_size_over_time import line_size_over_time

class MultiHistogram ():
    """Multi Histogram object that holds all data from a mutli species histogram.dat 
    to be interpreting in many different ways
    """

    def __init__(self,FileName: str, FileNum: int, InitialTime: float, FinalTime: float, SpeciesList: list):
        """Will initilize the object by reading through the inputted file(s)

        Args:
            FileName (str): file location (relative) histogram.dat that will be read
            FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
            InitialTime (float): The starting time. Must not be smaller / larger then times in file.
            FinalTime (float): The ending time. Must not be smaller / larger then times in file.
            SpeciesName (list): The names of the species you want to examine. Should be in the .dat file.
                Ex: ['a','b']     
        """

        #Initilize variables
        self.full_hist = []
        self.FileName = FileName
        self.FileNum = FileNum
        self.InitialTime = InitialTime
        self.FinalTime = FinalTime
        self.SpeciesList = SpeciesList
        
        #setup file naming
        file_name_head = FileName.split('.')[0]
        file_name_tail = FileName.split('.')[1]

        for histogram_file_number in range(1, FileNum+1):
            
            #determining file name (if there are multiple or none)
            if FileNum == 1:
                temp_file_name = FileName
            else:
                temp_file_name = file_name_head + '_' + str(histogram_file_number) + '.' + file_name_tail
            
            #load in the file
            temp_hist = read_multi_hist(temp_file_name,SpeciesList)
            self.full_hist.append(temp_hist)


    ##Number of complexes over time (2d)
    def line_mean_complex_size(self, SpeciesName: str, ExcludeSize: int = 0, ShowFig: bool = True, SaveFig: bool = False):
        """Creates graph of the mean number of species in a single complex molecule over a time period.

        Args:
            SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.
            ExcludeSize (int, optional): Monomers in the complex that are smaller or equal to this number will not be included. 
            ShowFig (bool, optional): If the plot is shown. Defaults to True.
            SaveFig (bool, optional): If the plot is saved. Defaults to False.

        Returns:
            graph. X-axis = time. Y
            -axis = mean number of species in a single complex molecule.
        """

        return line_size_over_time(Data = 1, full_hist = self.full_hist, FileNum = self.FileNum, InitialTime = self.InitialTime, FinalTime = self.FinalTime,
                SpeciesName = SpeciesName, ExcludeSize = ExcludeSize, SpeciesList = self.SpeciesList, ShowFig = ShowFig, SaveFig = SaveFig)

    def line_max_complex_size(self, SpeciesName: str, ExcludeSize: int = 0, ShowFig: bool = True, SaveFig: bool = False):
            """Creates graph of the mean number of species in a single complex molecule over a time period.

            Args:
                SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.
                ExcludeSize (int, optional): Monomers in the complex that are smaller or equal to this number will not be included. 
                ShowFig (bool, optional): If the plot is shown. Defaults to True.
                SaveFig (bool, optional): If the plot is saved. Defaults to False.

            Returns:
                graph. X-axis = time. Y
                -axis = mean number of species in a single complex molecule.
            """

            return line_size_over_time(Data = 2, full_hist = self.full_hist, FileNum = self.FileNum, InitialTime = self.InitialTime, FinalTime = self.FinalTime,
                    SpeciesName = SpeciesName, ExcludeSize = ExcludeSize, SpeciesList = self.SpeciesList, ShowFig = ShowFig, SaveFig = SaveFig)







