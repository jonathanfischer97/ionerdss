"""
Data processing module for ionerdss analysis.

Provides centralized data loading, processing, and caching capabilities.
"""

from .core import Data
from .processors import HistogramProcessor, CopyNumberProcessor, TransitionProcessor

__version__ = "2.0.0"
__all__ = ["Data", "HistogramProcessor", "CopyNumberProcessor", "TransitionProcessor"]