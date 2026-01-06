import streamlit as st
from fetch import fetch_data, process_data
from metrics import calculate_metrics
from indicators import add_technical_indicators
import plotly.graph_objects as go  # visualizations
import plotly.express as px  # visualizations
import sidebar

# update dashboard based on user input

if st.sidebar.button('Update Dashboard'):
    data = fetch_data(ticker, time_period, interval_mapping(time_period))
    data = process_data(data)
    data = add_technical_indicators(data, indicators)

    last_close, change, per_change, high, low, volume = calculate_metrics(data)

    # display metrics

    st.metric(label=f"{ticker} Last Close Price",
              value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({per_change:.2f}%) ")

    col1, col2, col3 = st.columns(3)
    col1.metric('High', f"{high:.2f} USD")
    col2.metric('Low', f"{low:.2f} USD")
    col3.metric('Volume', f"{volume:,}")

    # plot charts based on user selection

    fig = go.Figure()
    if chart_type == 'Candlestick Chart':
        fig.add_trace(go.Candlestick(x=data['Datetime'],
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close']))
    else:
        fig = px.line(data, x='Datetime', y='Close')

    # add technical indicators to the chart

    for indicator in indicators:
        if indicator == 'SMA 20':
            fig.add_trace(go.Scatter(
                x=data['Datetime'], y=data['SMA 20'], name='SMA 20'))
        elif indicator == 'EMA 20':
            fig.add_trace(go.Scatter(
                x=data['Datetime'], y=data['EMA 20'], name='EMA 20'))

    # format graph layout

    fig.update_layout(title=f"{ticker} {time_period.upper()} Chart",
                      xaxis_title='Time', yaxis_title='Price (USD)', height=600)

    st.plotly_chart(fig, use_container_width=True)

    # historical data and technical indicators

    st.subheader('Historical Data')
    st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])

    st.subheader('Technical Indicators')
    st.dataframe(data[['SMA 20', 'EMA 20']])
