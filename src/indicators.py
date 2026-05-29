import numpy as np  # numerical operations
import pandas as pd  # data manipulation

# part 3: function for numerical operations


def add_technical_indicators(data):
    data['SMA_20'] = data['Close'].rolling(window=20, min_periods=1).mean()
    data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()
    return data

# adding a vectorized backtester to check the SMA strategy performance across all the synthetic paths at once


def run_vectorized_backtest(paths, fast_window=20, slow_window=50):
    df_paths = pd.DataFrame(paths)
    sma_fast = df_paths.rolling(
        window=fast_window, min_periods=1).mean().values
    sma_slow = df_paths.rolling(
        window=slow_window, min_periods=1).mean().values

    signals = np.where(sma_fast > sma_slow, 1, -1)
    signals = np.roll(signals, shift=1, axis=0)
    signals[0] = 0

    asset_returns = np.diff(paths, axis=0) / paths[:-1]
    strategy_returns = signals[:-1] * asset_returns
    equity_curves = np.vstack(
        [np.ones(paths.shape[1]), np.cumprod(1 + strategy_returns, axis=0)])

    # Performance Math
    mean_ret = np.mean(strategy_returns, axis=0)
    std_ret = np.where(np.std(strategy_returns, axis=0) == 0,
                       1e-6, np.std(strategy_returns, axis=0))
    sharpes = (mean_ret / std_ret) * np.sqrt(252)

    running_max = np.maximum.accumulate(equity_curves, axis=0)
    drawdowns = np.min((equity_curves - running_max) / running_max, axis=0)
    final_returns = equity_curves[-1] - 1.0  # Final return over the year

    return sharpes, drawdowns, final_returns
