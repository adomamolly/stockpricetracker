## part 2: function for calculating key metrics##

def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    per_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    vol = data['Volume'].sum()
    return last_close, prev_close, change, per_change, high, low, vol
