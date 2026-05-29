import numpy as np

## part 2: function for calculating key metrics##


def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    per_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    vol = data['Volume'].sum()
    return last_close, change, per_change, high, low, vol


# adding a geometric brownian motion generator to create synthetic price arrays

def generate_gbm_paths(S0=100, mu=0.05, sigma=0.25, T=1.0, dt=1/252, n_paths=1000):
    n_steps = int(T / dt)
    paths = np.zeros((n_steps + 1, n_paths))
    paths[0] = S0
    Z = np.random.normal(0, 1, size=(n_steps, n_paths))
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    paths[1:] = S0 * np.exp(np.cumsum(drift + diffusion, axis=0))
    return paths
