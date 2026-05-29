from src.fetch import process_data, fetch_data
import streamlit as st  # for web app
from src.metrics import calculate_metrics  # for calculating key metrics

# Set page configuration/page layout

st.set_page_config(layout="wide")
st.title("Stock Price Tracker")

# Sidebar for user inputs

st.sidebar.header("User Input Features")
ticker = st.sidebar.text_input("Ticker Symbol", "AAPL")
time_period = st.sidebar.selectbox(
    "Time period", ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox(
    'Chart Type', ['Line Chart', 'Candlestick Chart'])
indicators = st.sidebar.multiselect(
    'Technical Indicators', ['SMA 20', 'EMA 20'])

# Mapping of time periods to data intervals

interval_mapping = {
    '1d': '1m',
    '1wk': '30m',
    '1mo': '1d',
    '1y': '1wk',
    'max': '1wk'
}

# Sidebar selection for real-time prices of selected symbols

st.sidebar.header('Real-Time Stock Prices')
stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
for symbol in stock_symbols:
    real_time_data = fetch_data(symbol, '1d', '1m')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        latest_price = real_time_data['Close'].iloc[-1]
        change = latest_price - real_time_data['Open'].iloc[-1]
        per_change = (change / real_time_data['Open']).iloc[0] * 100
        st.sidebar.metric(
            f"{symbol} Price", f"${latest_price:.2f} USD", f"{change:.2f} ({per_change})%")
