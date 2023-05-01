
from .heatmap import heatmap


def hist_3d_complex_count(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                 SpeciesName: str, TimeBins: int, xBarSize: int = 1, ShowFig: bool = True, SaveFig: bool = False):
    """Takes in a histogram.dat file from NERDSS, and creates a 3D histogram that represents the average number of monomers in each complex size, over time.

    Args:
        FileName (str): Path to the histogram.dat file
        FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.
        TimeBins (int): The number of bins that the selected time period is divided into.
        xBarSize (int, optional): The size of each data bar in the x-dimension. Defaults to 1.
        ShowFig (bool, optional): If the plot is shown. Defaults to True.
        SaveFig (bool, optional): If the plot is saved. Defaults to False.

    Returns:
        Returns a 3D histogram representing the number of monomers in a single complex over time. X-axis = species type/size. Y-axis = averaged time. Z-axis = relative occurance.
    """

    heatmap(2,1,FileName, FileNum, InitialTime, FinalTime,
            SpeciesName, TimeBins, xBarSize, ShowFig,
            False, False, SaveFig)