"""
This module provides an API for describing "grid-based" Markov Decision
Processes: MDPs whose state set is a grid of slots, and the transition scheme is
based on walking between adjacent slots in the grid, with a touch of randomness.
"""

from mdp.grid.grid_mdp import GridMDP
from mdp.grid.direction import directionToString
