from src.fetch import process_data, fetch_data
import streamlit as st
from src.metrics import calculate_metrics


def sidebar():
    """
    Wraps the sidebar widgets and returns user selections as a dictionary.
    Duplicates removed to prevent ElementID collisions.
    """
    # 1. Set page configuration/page layout
    st.set_page_config(layout="wide")
    st.title("Stock Price Tracker")

    # 2. Render input features ONCE (with unique keys just to be bulletproof)
    st.sidebar.header("User Input Features")
    ticker = st.sidebar.text_input(
        "Ticker Symbol", "AAPL", key="hist_ticker_input")
    time_period = st.sidebar.selectbox(
        "Time period", ['1d', '1wk', '1mo', '1y', 'max'], key="hist_time_period_select")
    chart_type = st.sidebar.selectbox(
        'Chart Type', ['Line Chart', 'Candlestick Chart'], key="hist_chart_type_select")
    indicators = st.sidebar.multiselect(
        'Technical Indicators', ['SMA_20', 'EMA_50'], key="hist_indicators_select")

    # 3. Mapping of time periods to data intervals
    interval_mapping = {
        '1d': '1m',
        '1wk': '30m',
        '1mo': '1d',
        '1y': '1wk',
        'max': '1wk'
    }

    # 4. Sidebar selection for real-time prices of selected symbols
    st.sidebar.header('Real-Time Stock Prices')
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    for symbol in stock_symbols:
        real_time_data = fetch_data(symbol, '1d', '1m')
        if not real_time_data.empty:
            real_time_data = process_data(real_time_data)

            # Extract individual scalar numbers cleanly out of the DataFrame
            latest_price = float(real_time_data['Close'].iloc[-1])
            initial_open = float(real_time_data['Open'].iloc[0])

            # Clean mathematical transformations using standard numbers
            change = latest_price - initial_open
            per_change = (change / initial_open) * 100

            # This will now format perfectly because all variables are single floats!
            st.sidebar.metric(
                f"{symbol} Price",
                f"${latest_price:.2f} USD",
                f"{change:.2f} ({per_change:.2f}%)"
            )

    # 5. Return configurations cleanly as a dictionary to mainc.py
    return {
        'ticker': ticker,
        'time_period': time_period,
        'chart_type': chart_type,
        'indicators': indicators,
        'interval_mapping': interval_mapping
    }
