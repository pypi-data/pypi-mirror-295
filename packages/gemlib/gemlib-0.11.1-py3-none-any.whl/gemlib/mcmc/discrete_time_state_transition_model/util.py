"""Utilities for DiscreteTimeStateTransitionModel MCMC kernels"""

from typing import NamedTuple


class TransitionTopology(NamedTuple):
    prev: int
    target: int
    next: int
