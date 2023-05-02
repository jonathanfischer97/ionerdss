from .read_multi_hist import read_multi_hist 
from ..line_size_over_time import line_size_over_time
from .multi_hist_complex_count import multi_hist_complex_count
from .multi_stack_hist_complex_count import multi_stack_hist_complex_count
from .multi_heatmap_complex_dist import multi_heatmap_complex_dist
from .multi_hist_3D_complex_dist import multi_hist_3D_complex_dist


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
            SpeciesName (list): The names of the species that are in the multi-histogram file
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


    ##Frequency of each complex size
    def hist_complex_count(self, BinNums: int = 10, ExcludeSize: int = 0, ShowFig: bool = True, SaveFig: bool = False):
        """ Creates a 3D heatmap from a histogram.dat (multi-species) that shows distrubution of sizes of selected species.

        Args:
            BinNums (int, optional): The number of bins in the histogram. Default is 10.
            ExcludeSize (int, optional): The minimum value required to include a data point in the histogram. Default is 0.
            ShowFig (bool, optional): Whether to display the generated figures. Default is True.
            SaveFig (bool, optional): Whether to save the generated figures. Default is False.

        Returns:
            3D Histogram. X-axis / Y-axis: the distribution of sizes of each specified species. Color: relative occurance of each complex.
        """

        return multi_hist_complex_count(self.FileName, self.FileNum, self.InitialTime, self.FinalTime, SpeciesList=self.SpeciesList,
                          BinNums=BinNums, ExcludeSize=ExcludeSize, ShowFig=ShowFig, SaveFig=SaveFig)



    ##Frequency of each kind of complex (stacked histogram)
    def stack_hist_complex_count(self,xAxis: str, DivideSpecies: str, DivideSize: int,
                        BarSize: int = 1, ExcludeSize: int = 0, ShowFig: bool = True, SaveFig: bool = False):
        """Creates a stacked histogram from histogram.dat (multi-species) that shows the average number of each type of 
        complex species (based on protein composition) over the whole sim. 

        Args:
            xAxis (str): Species shown on X-axis.
            DivideSpecies (str): The name of the species that will be seperated by size.
            DivideSize (int): The value that separates the size of dissociate complexes. (only changes color of graph)
            BarSize (int, optional): The size of each data bar in the X-dimension. Defaults to 1.
            ExcludeSize (int, optional): Monomers in the complex that are smaller or equal to this number will not be included. 
            ShowFig (bool, optional): If the plot is shown. Defaults to True.
            SaveFig (bool, optional): If the plot is saved. Defaults to False.
        Returns:
            Histogram. X-axis = size of selected species, Y-axis = average number of each corresponds.
        """

        return multi_stack_hist_complex_count(FileName=self.FileName, FileNum=self.FileNum, InitialTime= self.InitialTime, FinalTime = self.FinalTime, SpeciesList=self.SpeciesList, 
                                  xAxis=xAxis, DivideSpecies=DivideSpecies, DivideSize=DivideSize, BarSize=BarSize,ExcludeSize=ExcludeSize, ShowFig=ShowFig, SaveFig=SaveFig)


    ##Average count of each complex composition over the entire simulation time
    def heatmap_complex_dist(self,xAxis: str, yAxis: str, SpeciesList: list = [], xBarSize: int = 1, yBarSize: int = 1,
                    ShowFig: bool = True, ShowMean: bool = False, ShowStd: bool = False, SaveFig: bool = False):
        """ Creates a 3D heatmap from a histogram.dat (multi-species) that shows distrubution of sizes of selected species.

        Args:
            xAxis (str): Species shown on X-axis.
            yAxis (str): Species shown on Y-axis.
            xBarSize (int, optional): The size of each data bar in the X-dimension. Defaults to 1.
            yBarSize (int, optional): The size of each data bar in the Y-dimension. Defaults to 1.
            ShowMean (bool, optional): If means will be shown in each box. Defaults to False.
            ShowStd (bool, optional): If std values will be shown in each box. Defaults to False.
            ShowFig (bool, optional): If the plot is shown. Defaults to True.
            SaveFig (bool, optional): If the plot is saved. Defaults to False.

        Returns:
            3D Histogram. X-axis / Y-axis: the distribution of sizes of each specified species. Color: relative occurance of each complex.
        """

        return multi_heatmap_complex_dist(FileName=self.FileName, FileNum=self.FileNum, InitialTime=self.InitialTime, FinalTime=self.FinalTime, xAxis=xAxis, yAxis=yAxis,
                             SpeciesList=SpeciesList, xBarSize=xBarSize, yBarSize=yBarSize, ShowFig=ShowFig, ShowMean=ShowMean,
                             ShowStd=ShowStd, SaveFig=SaveFig)
    

    def hist_3D_complex_dist(self,xAxis: str, yAxis: str, SpeciesList: list = [], xBarSize: int = 1, yBarSize: int = 1,
                    ShowFig: bool = True, SaveFig: bool = False):
        """ Creates a 3D heatmap from a histogram.dat (multi-species) that shows distrubution of sizes of selected species.

        Args:
            xAxis (str): Species shown on X-axis.
            yAxis (str): Species shown on Y-axis.
            xBarSize (int, optional): The size of each data bar in the X-dimension. Defaults to 1.
            yBarSize (int, optional): The size of each data bar in the Y-dimension. Defaults to 1.
            ShowMean (bool, optional): If means will be shown in each box. Defaults to False.
            ShowStd (bool, optional): If std values will be shown in each box. Defaults to False.
            ShowFig (bool, optional): If the plot is shown. Defaults to True.
            SaveFig (bool, optional): If the plot is saved. Defaults to False.

        Returns:
            3D Histogram. X-axis / Y-axis: the distribution of sizes of each specified species. Color: relative occurance of each complex.
        """

        return multi_hist_3D_complex_dist(FileName=self.FileName, FileNum=self.FileNum, InitialTime=self.InitialTime, FinalTime=self.FinalTime, xAxis=xAxis, yAxis=yAxis,
                             SpeciesList=SpeciesList, xBarSize=xBarSize, yBarSize=yBarSize, ShowFig=ShowFig, SaveFig=SaveFig)




