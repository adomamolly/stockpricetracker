import streamlit as st  # for web app

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
