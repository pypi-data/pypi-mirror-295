def generate_trade_summary(trades):
    """ Generate a summary of trading performance. """
    win_trades = trades[trades['trade_return_hist'] > 0]
    lose_trades = trades[trades['trade_return_hist'] <= 0]

    summary = {
        'Total Trades': len(trades),
        'Winning Trades': len(win_trades),
        'Losing Trades': len(lose_trades),
        'Win Rate': len(win_trades) / len(trades) if len(trades) > 0 else None,
        'Average Win': win_trades['trade_return_hist'].mean(),
        'Average Loss': lose_trades['trade_return_hist'].mean(),
        'Profit Factor': win_trades['trade_return_hist'].sum() / abs(lose_trades['trade_return_hist'].sum()) if len(lose_trades) > 0 else None
    }
    return summary


def calculate_volatility_clustering(data, window=20):
    """ Calculate volatility clustering based on rolling standard deviation. """
    volatility = data.pct_change().rolling(window=window).std()
    periods_of_clustering = volatility[volatility > volatility.mean() + 2 * volatility.std()]
    return periods_of_clustering


def plot_monte_carlo_simulation(simulations, title="Monte Carlo Simulations", save=False):
    """ Plot multiple equity paths from a Monte Carlo simulation. """
    plt.figure(figsize=(10, 6))
    plt.plot(simulations, color='blue', alpha=0.1)  # Light blue lines for individual simulations
    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Equity Value')
    plt.grid(True)

    # Plot mean and confidence intervals
    mean_path = simulations.mean(axis=1)
    plt.plot(mean_path, color='red', linewidth=2, label='Mean Equity Path')

    if save:
        plt.savefig(f'{title}.png', dpi=300)

    plt.legend()
    plt.show()


def monte_carlo_simulation(initial_balance, mean_return, std_dev, n_days=252, n_simulations=1000):
    """ Perform a Monte Carlo simulation for equity curve evolution. """
    simulations = []
    for _ in range(n_simulations):
        daily_returns = np.random.normal(loc=mean_return, scale=std_dev, size=n_days)
        price_series = initial_balance * (1 + daily_returns).cumprod()
        simulations.append(price_series)

    simulations = pd.DataFrame(simulations).T  # Simulations become columns
    return simulations


def equity_curve_analysis(data, risk_free_rate=0):
    """ Analyze an equity curve and calculate multiple performance metrics. """
    total_ret = total_return(data)
    annual_ret = annualized_return(data)
    sharpe = sharpe_ratio(data.pct_change(), risk_free_rate)
    max_dd, peak, trough = calculate_max_drawdown(data)

    analysis = {
        'Total Return': total_ret,
        'Annualized Return': annual_ret,
        'Sharpe Ratio': sharpe,
        'Max Drawdown': max_dd,
        'Drawdown Peak': peak,
        'Drawdown Trough': trough
    }
    return analysis


def calculate_max_drawdown(data):
    """ Calculate the maximum drawdown of a time series. """
    running_max = data.cummax()
    drawdowns = (data - running_max) / running_max
    max_drawdown = drawdowns.min()

    drawdown_periods = drawdowns[drawdowns < 0]
    peak = drawdown_periods.idxmin()
    trough = drawdown_periods.idxmax()

    return max_drawdown, peak, trough


def optimize_parameters(data, strategy_func, parameter_grid, metric='sharpe'):
    """ Optimize strategy parameters by running multiple backtests and choosing the best based on the metric. """
    best_params = None
    best_metric = -np.inf
    results = []

    # Iterate through all combinations of parameters
    for params in parameter_grid:
        result = strategy_func(data, **params)

        # Choose the appropriate metric to compare
        if metric == 'sharpe':
            current_metric = sharpe_ratio(result['equity_curve'].pct_change())
        elif metric == 'return':
            current_metric = total_return(result['equity_curve'])
        else:
            raise ValueError("Unsupported metric. Use 'sharpe' or 'return'.")

        # Track best parameters and results
        if current_metric > best_metric:
            best_metric = current_metric
            best_params = params
        results.append((params, current_metric))

    return best_params, results
