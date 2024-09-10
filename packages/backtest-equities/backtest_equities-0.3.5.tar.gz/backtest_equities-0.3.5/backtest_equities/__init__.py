# __init__.py

from .backtest import run_backtest_and_analysis, backtest_over_periods, backtest_run
from .period_split import split_periods
from .optimization import optimize_parameters
from .analysis import equity_curve_analysis, monte_carlo_simulation, plot_monte_carlo_simulation

__all__ = [
    "run_backtest_and_analysis",
    "backtest_over_periods",
    "backtest_run",
    "split_periods",
    "optimize_parameters",
    "equity_curve_analysis",
    "monte_carlo_simulation",
    "plot_monte_carlo_simulation",
]

__author__ = "Jack Martin"
__license__ = "Unlicense"
