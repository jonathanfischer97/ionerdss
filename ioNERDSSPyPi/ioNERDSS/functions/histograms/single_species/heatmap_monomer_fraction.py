import numpy as np
import matplotlib.pyplot as plt
from .heatmap import heatmap


def heatmap_monomer_fraction(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                               SpeciesName: str, TimeBins: int, xBarSize: int = 1, ShowFig: bool = True,
                               ShowMean: bool = False, ShowStd: bool = False, SaveFig: bool = False):
    """Generates a 2D histogram from histogram.dat of the % of the original monomers forming into different complex sizes over time

    Args:
        FileName (str): file location (relative) histogram.dat that will be read
        FileNum (int): Number of the total input files (file names should be [fileName]_1,[fileName]_2,...)
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.        
        TimeBins (int): The number of bins that the selected time period is divided into.
        xBarSize (int, optional): The size of each data bar in the x-dimension. Defaults to 1.
        ShowFig (bool, optional): If the plot is shown. Defaults to True.
        ShowMean (bool, optional): If means will be shown in each box. Defaults to False.
        ShowStd (bool, optional): If std values will be shown in each box. Defaults to False.
        SaveFig (bool, optional): If the plot is saved. Defaults to False.

    Returns:
        2D heatnao. X-axis = complex species size. Y-axis = time. Color = fraction of monomers forming into that complex at that time
    """
    
    heatmap(1,3,FileName, FileNum, InitialTime, FinalTime,
            SpeciesName, TimeBins, xBarSize, ShowFig,
            ShowMean, ShowStd, SaveFig)