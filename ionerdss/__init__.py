from .model_setup import *
from .analysis import *

import seaborn as sns

# Set the figure style using Seaborn
fontsize = 12
sns.set_style("ticks")
sns.set_context("paper", rc={
    "font.size": fontsize,
    "axes.titlesize": fontsize,
    "axes.labelsize": fontsize,
    "xtick.labelsize": fontsize,
    "ytick.labelsize": fontsize,
    "legend.fontsize": fontsize,
    "font.family": "serif"
})