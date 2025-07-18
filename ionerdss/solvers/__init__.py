"""
ionerdss.solvers - Mathematical solvers and equation systems.

This module provides solvers for various mathematical systems including
ODE systems and reaction kinetics.

Main functions:
    solve_reaction_ode: Solve reaction ODE systems
    ReactionStringParser: Parse reaction string notations
"""

from .reaction_ode_solver import solve_reaction_ode, dydt, calculate_macroscopic_reaction_rates
from .reaction_string_parser import ReactionStringParser

__all__ = ['solve_reaction_ode', 'dydt', 'calculate_macroscopic_reaction_rates', 'ReactionStringParser']