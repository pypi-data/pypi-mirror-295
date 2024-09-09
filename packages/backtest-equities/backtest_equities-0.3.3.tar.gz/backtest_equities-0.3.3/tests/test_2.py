import numpy as np
import pandas as pd
from your_backtest_module import (
    run_backtest_and_analysis, equity_curve_analysis,
    monte_carlo_simulation, plot_monte_carlo_simulation,
    generate_trade_summary, calculate_volatility_clustering
)

# Test 1: Basic Backtest
def test_basic_backtest():
    """ Test running a basic backtest with default parameters. """
    data = load_your_data()  # Load sample test data
    side = 'long'
    SL_type = 'fixed'
    SL = 0.02
    SL_spike_out = None
    TP = 0.04
    TS = 0.01

    results = run_backtest_and_analysis(data, side, SL_type, SL, SL_spike_out, TP, TS)

    assert results is not None, "Backtest results should not be None"
    assert len(results) > 0, "Backtest should return results for each period"

    # Validate the first result in backtest
    analysis = equity_curve_analysis(results[0][11]['equity_curve'])
    assert 'Sharpe Ratio' in analysis, "Equity curve analysis should include Sharpe Ratio"


# Test 2: Parameter Optimization
def test_parameter_optimization():
    """ Test optimizing strategy parameters. """
    data = load_your_data()  # Load sample test data
    side = 'long'
    SL_type = 'fixed'
    SL = 0.02
    SL_spike_out = None
    TP = 0.04
    TS = 0.01

    strategy_params = [
        {'side': 'long', 'SL_type': 'fixed', 'SL': 0.02, 'TP': 0.04, 'TS': 0.01},
        {'side': 'short', 'SL_type': 'fixed', 'SL': 0.01, 'TP': 0.03, 'TS': 0.01}
    ]

    best_params, optimization_results = run_backtest_and_analysis(data, side, SL_type, SL, SL_spike_out, TP, TS, optimize=True, strategy_params=strategy_params)

    assert best_params is not None, "Optimization should return best parameters"
    assert len(optimization_results) == len(strategy_params), "Optimization results should match parameter set length"


# Test 3: Monte Carlo Simulation
def test_monte_carlo_simulation():
    """ Test Monte Carlo simulation for equity curve evolution. """
    initial_balance = 10000
    mean_return = 0.001  # 0.1% daily return
    std_dev = 0.02  # 2% daily volatility
    n_days = 252
    n_simulations = 1000

    simulations = monte_carlo_simulation(initial_balance, mean_return, std_dev, n_days, n_simulations)
    assert simulations.shape == (n_days, n_simulations), "Simulation should return correct shape"
    assert not simulations.isna().any().any(), "Simulation data should not contain NaN values"

    # Test the plot function
    plot_monte_carlo_simulation(simulations, title="Monte Carlo Simulation Test", save=False)


# Test 4: Trade Summary Generation
def test_trade_summary_generation():
    """ Test generating a trade summary from historical trades. """
    trades = pd.DataFrame({
        'trade_return_hist': [0.05, -0.02, 0.03, -0.01, 0.08, -0.04]
    })

    summary = generate_trade_summary(trades)

    assert summary['Total Trades'] == 6, "Total number of trades should be correct"
    assert summary['Winning Trades'] == 3, "Number of winning trades should be correct"
    assert summary['Losing Trades'] == 3, "Number of losing trades should be correct"
    assert summary['Win Rate'] == 0.5, "Win rate should be correct"
    assert summary['Profit Factor'] > 1, "Profit factor should be positive"


# Test 5: Volatility Clustering
def test_volatility_clustering():
    """ Test detecting periods of volatility clustering. """
    data = pd.Series(np.random.normal(0, 0.01, 500))  # Simulated time series data
    periods_of_clustering = calculate_volatility_clustering(data)

    assert periods_of_clustering is not None, "Volatility clustering should return a result"
    assert len(periods_of_clustering) > 0, "There should be periods of volatility clustering in random data"

# Running tests
if __name__ == "__main__":
    test_basic_backtest()
    test_parameter_optimization()
    test_monte_carlo_simulation()
    test_trade_summary_generation()
    test_volatility_clustering()

    print("All tests passed!")
