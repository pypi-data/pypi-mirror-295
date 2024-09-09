def validate_inputs(info, periods_for_split, split_years, side, SL_type, SL, SL_spike_out, TP, TS):
    """Validate user inputs before running backtests."""
    # Ensure that data is provided
    if info is None or info.empty:
        raise ValueError("Data cannot be empty or None.")

    # Validate split parameters
    valid_splits = ['yearly', 'biannually', 'quarterly', 'monthly', 'weekly', 'daily']
    if periods_for_split not in valid_splits:
        raise ValueError(f"Invalid period split: {periods_for_split}. Choose from {valid_splits}.")

    # Ensure split_years is positive for yearly split
    if periods_for_split == 'yearly' and split_years <= 0:
        raise ValueError("Split years must be a positive integer when splitting by years.")

    # Validate strategy parameters
    if side not in ['long', 'short', 'both']:
        raise ValueError("Invalid 'side'. Choose from 'long', 'short', or 'both'.")

    if SL_type not in ['fixed', 'trailing']:
        raise ValueError(f"Invalid 'SL_type': {SL_type}. Must be either 'fixed' or 'trailing'.")

    if not isinstance(SL, (int, float)) or SL <= 0:
        raise ValueError("Stop Loss (SL) must be a positive number.")

    if not isinstance(TP, (int, float)) or TP <= 0:
        raise ValueError("Take Profit (TP) must be a positive number.")

    if not isinstance(SL_spike_out, (int, float)):
        raise ValueError("SL spike-out should be a numeric value.")

    # Verify the trailing stop condition
    if SL_type == 'trailing' and (TS is None or TS <= 0):
        raise ValueError("When using trailing stop loss, TS (Trailing Stop) must be a positive number.")

    return True


def split_periods(info):
    """ Split the data into different periods based on the chosen period."""
    if not periods_for_split:
        return [info]

    # Ensure the DataFrame index is a DatetimeIndex
    if not isinstance(info.index, pd.DatetimeIndex):
        raise ValueError("The DataFrame index must be a DatetimeIndex.")

    if periods_for_split == 'yearly':
        if split_years <= 1:
            return [info.loc[info.index.year == year] for year in info.index.year.unique()]
        else:
            periods_info = []
            start_year = info.index.year.min()
            end_year = info.index.year.max()
            for year in range(start_year, end_year + 1, split_years):
                period_data = info.loc[(info.index.year >= year) & (info.index.year < year + split_years)]
                if not period_data.empty:
                    periods_info.append(period_data)
            if not periods_info:
                periods_info.append(info)
            return periods_info

    elif periods_for_split == 'biannually':
        periods_info = [info.loc[(info.index.year == year) & (info.index.month <= 6)] for year in
                        info.index.year.unique()] + \
                       [info.loc[(info.index.year == year) & (info.index.month > 6)] for year in
                        info.index.year.unique()]

    elif periods_for_split == 'quarterly':
        periods_info = [info.loc[(info.index.year == year) & (info.index.quarter == q)] for year in
                        info.index.year.unique() for q in range(1, 5)]

    elif periods_for_split == 'monthly':
        periods_info = [info.loc[(info.index.year == year) & (info.index.month == month)] for year in
                        info.index.year.unique() for month in range(1, 13)]

    elif periods_for_split == 'weekly':
        week_starts = info.index.tz_localize(None).to_period('W').start_time
        periods_info = [info.loc[week_starts == week_start] for week_start in week_starts.unique()]

    elif periods_for_split == 'daily':
        unique_dates = pd.Index(info.index.date).unique()
        periods_info = [info.loc[info.index.date == date] for date in unique_dates]

    else:
        raise ValueError(
            f"{periods_for_split} is an unsupported period. Choose from 'yearly', 'biannually', 'quarterly', 'monthly', 'weekly', 'daily'.")

    periods_info = [x for x in periods_info if not x.empty]
    return sorted(periods_info, key=lambda x: x.index[0])


def backtest_over_periods(info, side, SL_type, SL, SL_spike_out, TP, TS):
    """ Run a backtest on a given strategy over different periods and return the results."""
    output = []
    for period_info in info:
        if len(period_info) > 0:
            output.append(backtest_run(period_info, side, SL_type, SL, SL_spike_out, TP, TS))
    return output


def backtest_run(info, side, SL_type, SL, SL_spike_out, TP, TS):
    """ Run a backtest on strategy and return the results.
    Outer scope variables ok. """
    bt = Backtest(info, side, SL_type, SL, SL_spike_out, TP, TS)
    backtest_result = bt.run()
    ev_ratio, winR, RR = ev_calculator(backtest_result, SL_type)
    trade_details = trade_details_generator(backtest_result.copy())

    period_start = backtest_result.index[0]
    period_end = backtest_result.index[-1]
    no_trades = len(backtest_result[backtest_result['trade_length_hist'] == 1]) if not backtest_result[
        backtest_result['trade_length_hist'] == 1].empty else len(backtest_result[~backtest_result['win'].isna()])
    trading_frequency = round(len(backtest_result) / no_trades, 0) if no_trades != 0 else None  # puts on a trade every x mins, hours, days, etc. on average.
    occupancy = len(backtest_result[backtest_result['trade_length_hist'] != 0]) / len(backtest_result)

    total_return = backtest_result['equity_curve'].iloc[-1] / bt.initial_balance - 1
    max_drawdown = backtest_result['drawdown'].max()

    returns = backtest_result['equity_curve'].pct_change(fill_method=None).dropna()
    long_returns = backtest_result['long_equity_curve'].pct_change(fill_method=None).dropna()
    short_returns = backtest_result['short_equity_curve'].pct_change(fill_method=None).dropna()
    sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if not np.isnan(returns.std()) and returns.std() != 0 else None
    long_sharpe_ratio = long_returns.mean() / long_returns.std() * np.sqrt(252) if not np.isnan(long_returns.std()) and long_returns.std() != 0 else None
    short_sharpe_ratio = short_returns.mean() / short_returns.std() * np.sqrt(252) if not np.isnan(short_returns.std()) and short_returns.std() != 0 else None
    trade_returns = backtest_result[~backtest_result['trade_return_hist'].isna()]['trade_return_hist']
    adj_sharpe_ratio = trade_returns.mean() / trade_returns.std() * np.sqrt(252) if len(trade_returns) > 0 and not np.isnan(trade_returns.std()) and trade_returns.std() != 0 else None
    # Sensitive: if we deal only with ongoing trades or no_trades=1, adj_sharpe_ratio is None, but EV and R will be calculated based on return.

    return (
        period_start, period_end,
        side, SL_type, SL, TP, TS,
        no_trades, trading_frequency, occupancy,
        bt, backtest_result, total_return, max_drawdown,
        sharpe_ratio, long_sharpe_ratio, short_sharpe_ratio,
        adj_sharpe_ratio, ev_ratio, winR, RR,
        trade_details)


order_return_backtest_run = (
    'period_start', 'period_end',
    'side', 'SL_type', 'SL', 'TP', 'TS',
    'no_trades', 'trading_frequency', 'occupancy',
    'bt', 'backtest_result', 'total_return', 'max_drawdown',
    'sharpe_ratio', 'long_sharpe_ratio', 'short_sharpe_ratio',
    'adj_sharpe_ratio', 'ev_ratio', 'winR', 'RR',
    'trade_details')
order_return_trade_details_generator = (
    "open2close", "open2high", "open2low",
    "open2close_max", "open2high_max", "open2low_max",
    "open2close_min", "open2high_min", "open2low_min",
    "open2close_win", "open2high_win", "open2low_win",
    "open2close_win_max", "open2high_win_max", "open2low_win_max",
    "open2close_win_min", "open2high_win_min", "open2low_win_min",
    "open2close_noWin", "open2high_noWin", "open2low_noWin",
    "open2close_noWin_max", "open2high_noWin_max", "open2low_noWin_max",
    "open2close_noWin_min", "open2high_noWin_min", "open2low_noWin_min"
)
order_return_backtest_run = {key: i for i, key in enumerate(order_return_backtest_run)}
order_return_trade_details_generator = {key: i for i, key in enumerate(order_return_trade_details_generator)}


def alternative_equity_curves(strat_name, side, backtest_result, bt, path, no_equity_curves=5, save=False, quiet=True):
    # Verification: Trade distribution
    only_trades = backtest_result[['long_shares_curve', 'short_shares_curve', 'trade_idx_hist', 'trade_return_hist']].copy()
    only_trades['trade_return_hist_f1'] = only_trades['trade_return_hist'].shift(-1)
    mask = only_trades['trade_return_hist_f1'].isna()
    # Any ongoing trades will not be included since it's outcome is not known yet.
    only_trades = only_trades.loc[~mask]
    only_trades.drop(columns=['trade_return_hist'], inplace=True)

    if side == 'short':
        long_investment = 0
        short_investment = bt.initial_balance
    elif side == 'long':
        long_investment = bt.initial_balance
        short_investment = 0
    else:
        long_investment = bt.initial_balance / 2
        short_investment = bt.initial_balance / 2
    long_trade_returns = only_trades[only_trades['long_shares_curve'] > 0]['trade_return_hist_f1']
    short_trade_returns = only_trades[only_trades['short_shares_curve'] > 0]['trade_return_hist_f1']

    long_realized_equity = long_investment * (1 + long_trade_returns).cumprod()
    short_realized_equity = short_investment * (1 + short_trade_returns).cumprod()
    long_realized_equity_idx_org = long_realized_equity.index
    short_realized_equity_idx_org = short_realized_equity.index
    combined_index = long_realized_equity.index.union(short_realized_equity.index)
    long_realized_equity = long_realized_equity.reindex(combined_index)
    short_realized_equity = short_realized_equity.reindex(combined_index)
    if not long_realized_equity.empty and pd.isna(long_realized_equity.iloc[0]):
        long_realized_equity.iloc[0] = long_investment
    if not short_realized_equity.empty and pd.isna(short_realized_equity.iloc[0]):
        short_realized_equity.iloc[0] = short_investment
    only_trades['realized_equity'] = pd.concat([long_realized_equity.ffill(), short_realized_equity.ffill()],
                                               axis=1).sum(axis=1)

    np.random.seed(42)
    for i in range(0, no_equity_curves):
        shuffled_long_trade_returns = long_trade_returns.sample(frac=1).reset_index(drop=True)
        shuffled_short_trade_returns = short_trade_returns.sample(frac=1).reset_index(drop=True)
        long_shuffled_equity = long_investment * (1 + shuffled_long_trade_returns).cumprod()
        short_shuffled_equity = short_investment * (1 + shuffled_short_trade_returns).cumprod()
        long_shuffled_equity.index = long_realized_equity_idx_org
        short_shuffled_equity.index = short_realized_equity_idx_org
        combined_index = long_shuffled_equity.index.union(short_shuffled_equity.index)
        long_shuffled_equity = long_shuffled_equity.reindex(combined_index)
        short_shuffled_equity = short_shuffled_equity.reindex(combined_index)
        if not long_shuffled_equity.empty and pd.isna(long_shuffled_equity.iloc[0]):
            long_shuffled_equity.iloc[0] = long_investment
        if not short_shuffled_equity.empty and pd.isna(short_shuffled_equity.iloc[0]):
            short_shuffled_equity.iloc[0] = short_investment
        only_trades[f'shuffled_equity_{i}'] = pd.concat([long_shuffled_equity.ffill(), short_shuffled_equity.ffill()],
                                                        axis=1).sum(axis=1)

    plt.figure(figsize=(10, 6))
    equity_curves = only_trades.filter(like='shuffled_equity_')
    for column in equity_curves.columns:
        plt.plot(equity_curves.index, equity_curves[column], alpha=0.4)
    plt.plot(equity_curves.index, only_trades['realized_equity'], label='realized', linewidth=2.5)
    # Since only trades are incl., starting point might be different for each altEquityCurve.
    # There might be end-of-period differences between the realized equity curves
    # and the market-to-market equity curve since realized A. do not include ongoing trades, and B. does not plot intra-trade variations.
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Equity ($)')
    plt.title(f'{strat_name}: Shuffled Equity Curves for ${ticker}')
    plt.grid(True)
    if save:
        plt.savefig(f'{path}/{ticker}_{timeframe}_altEquity_{strat_name}.png', dpi=1200)
    if not quiet:
        plt.show()
    plt.close()

    return only_trades


# Calculate total return
def total_return(data):
    return data.iloc[-1] / data.iloc[0] - 1

# Calculate cumulative returns
def cumulative_returns(data):
    return (1 + data.pct_change()).cumprod() - 1

# Sharpe ratio calculation
def sharpe_ratio(returns, risk_free_rate=0):
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

# Sortino ratio calculation
def sortino_ratio(returns, risk_free_rate=0):
    downside = returns[returns < 0].std()
    return (returns.mean() - risk_free_rate) / downside * np.sqrt(252)

# Calculate rolling return
def rolling_return(data, window):
    return data.pct_change().rolling(window=window).sum()

# Max/min value over a given period
def max_value(data, window):
    return data.rolling(window=window).max()

def min_value(data, window):
    return data.rolling(window=window).min()

# Annualized return
def annualized_return(data):
    total_return_val = total_return(data)
    n_years = len(data) / 252  # Assume 252 trading days
    return (1 + total_return_val) ** (1 / n_years) - 1

# Drawdown calculation
def drawdown(data):
    running_max = data.cummax()
    return (data - running_max) / running_max

# Win rate calculation
def win_rate(trades):
    wins = trades[trades['trade_return_hist'] > 0]
    return len(wins) / len(trades)

# Average trade return
def avg_trade_return(trades):
    return trades['trade_return_hist'].mean()

# Calculate correlation between two assets
def correlation(asset1, asset2):
    return asset1.pct_change().corr(asset2.pct_change())

# Calculate rolling volatility
def rolling_volatility(data, window):
    return data.pct_change().rolling(window=window).std()

# Calculate CAGR (Compound Annual Growth Rate)
def cagr(data):
    n_years = len(data) / 252
    return (data.iloc[-1] / data.iloc[0]) ** (1 / n_years) - 1

