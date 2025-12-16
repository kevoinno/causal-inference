"""
Difference-in-Differences (DiD) Methods Package

This package provides tools for conducting difference-in-differences analysis,
including simulation, estimation, and visualization functions.
"""

from .did import (
    simulate,
    estimate_did,
    placebo_test,
    panel_plot,
    mean_outcomes_plot,
    means_plot,
    bias_visualization
)

__all__ = [
    'simulate',
    'estimate_did',
    'placebo_test',
    'panel_plot',
    'mean_outcomes_plot',
    'means_plot',
    'bias_visualization'
]

