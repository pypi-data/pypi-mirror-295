
def run_backtest_and_analysis(info, side, SL_type, SL, SL_spike_out, TP, TS, optimize=False, metrics='sharpe', strategy_params=None):
    """ Run the backtest, analyze results, and optionally optimize parameters. """
    print("Running backtest over split periods...")
    periods_info = split_periods(info)
    backtest_results = backtest_over_periods(periods_info, side, SL_type, SL, SL_spike_out, TP, TS)

    # If optimization is enabled, optimize the strategy parameters
    if optimize and strategy_params is not None:
        print("Optimizing strategy parameters...")
        best_params, optimization_results = optimize_parameters(info, backtest_run, strategy_params, metric=metrics)
        print(f"Best Parameters: {best_params}")
        return best_params, optimization_results

    # Analyze the results
    for result in backtest_results:
        _, _, _, _, _, _, _, _, _, _, bt, backtest_result, total_ret, max_dd, sharpe, long_sharpe, short_sharpe, adj_sharpe, ev_ratio, winR, RR, trade_details = result

        # Run equity curve analysis
        analysis = equity_curve_analysis(backtest_result['equity_curve'])
        print(f"Period Start: {result[0]}, Period End: {result[1]}")
        print(f"Total Return: {analysis['Total Return']}, Sharpe Ratio: {analysis['Sharpe Ratio']}, Max Drawdown: {analysis['Max Drawdown']}")

        # Run Monte Carlo simulation for risk assessment
        simulations = monte_carlo_simulation(bt.initial_balance, backtest_result['equity_curve'].pct_change().mean(),
                                             backtest_result['equity_curve'].pct_change().std())
        plot_monte_carlo_simulation(simulations, title=f"Monte Carlo Simulations for {result[0]} - {result[1]}")

    # Return the backtest results for further inspection
    return backtest_results


# Example Usage
if __name__ == "__main__":
    # Set your data and backtest parameters here
    data = load_your_data()  # Placeholder for your data loading function
    side = 'long'
    SL_type = 'fixed'
    SL = 0.02
    SL_spike_out = None
    TP = 0.04
    TS = 0.01

    # If you want to optimize
    strategy_params = [
        {'side': 'long', 'SL_type': 'fixed', 'SL': 0.02, 'TP': 0.04, 'TS': 0.01},
        {'side': 'short', 'SL_type': 'fixed', 'SL': 0.01, 'TP': 0.03, 'TS': 0.01},
        # Add more parameter sets for optimization if needed
    ]

    # Run backtest and analysis
    results = run_backtest_and_analysis(data, side, SL_type, SL, SL_spike_out, TP, TS, optimize=True, strategy_params=strategy_params)
