import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from yfinance import Ticker
from src.fetch import fetch_data, process_data
from src.metrics import calculate_metrics, generate_gbm_paths  # Added GBM import
# Added Backtest import
from src.indicators import add_technical_indicators
# Importing the sidebar layout function
from visuals.sidebar_layout import sidebar
# Added backtest function import
from src.indicators import run_vectorized_backtest

# ==============================================================================
# 1. ARCHITECTURE MODE SELECTOR (Placed at the absolute top of the sidebar)
# ==============================================================================
analysis_mode = st.sidebar.radio(
    "Select System Engine",
    ["Historical Ticker Analytics",
        "Synthetic Market Stress Test (Monte Carlo)"], key="selected_engine"
)

if analysis_mode == "Historical Ticker Analytics":
    # --------------------------------------------------------------------------
    # MODE A: YOUR ORIGINAL HISTORICAL DASHBOARD FLOW
    # --------------------------------------------------------------------------
    params = sidebar()
    if isinstance(params, dict):
        ticker = params.get('ticker', 'AAPL')
        time_period = params.get('time_period', '1mo')
        chart_type = params.get('chart_type', 'Line Chart')
        indicators = params.get('indicators', [])
        interval_mapping = params.get('interval_mapping', {time_period: '1d'})
    else:
        try:
            ticker, time_period, chart_type, indicators, interval_mapping = params
        except Exception:
            ticker = 'AAPL'
            time_period = '1mo'
            chart_type = 'Line Chart'
            indicators = []
            interval_mapping = {time_period: '1d'}

    if st.sidebar.button('Update Dashboard'):
        data = fetch_data(ticker, time_period, interval_mapping[time_period])
        data = process_data(data)
        data = add_technical_indicators(data)

        last_close, prev_close, change, per_change, high, low, vol = calculate_metrics(
            data)

        # 2. CRITICAL: Extract the single scalar value from each pandas Series
        last_close = float(
            last_close.iloc[-1]) if hasattr(last_close, "iloc") else float(last_close)
        change = float(
            change.iloc[-1]) if hasattr(change, "iloc") else float(change)
        per_change = float(
            per_change.iloc[-1]) if hasattr(per_change, "iloc") else float(per_change)
        high = float(high.iloc[-1]) if hasattr(high, "iloc") else float(high)
        low = float(low.iloc[-1]) if hasattr(low, "iloc") else float(low)
        volume = int(vol.iloc[-1]) if hasattr(vol, "iloc") else int(vol)

        # 3. Display metrics (This line 56 will now work flawlessly!)
        st.metric(
            label=f"{ticker} Last Close Price",
            value=f"{last_close:.2f} USD",
            delta=f"{change:.2f} ({per_change:.2f}%) "
        )

        # 4. Display columns using the corrected single variables
        col1, col2, col3 = st.columns(3)
        col1.metric('High', f"{high:.2f} USD")
        col2.metric('Low', f"{low:.2f} USD")
        col3.metric('Volume', f"{volume:,}")

        fig = go.Figure()
        if chart_type == 'Candlestick Chart':
            fig.add_trace(go.Candlestick(x=data['Datetime'], open=data['Open'],
                                         high=data['High'], low=data['Low'], close=data['Close']))
        else:
            fig = px.line(data, x='Datetime', y='Close')

        for indicator in indicators:
            if indicator == 'SMA 20':
                fig.add_trace(go.Scatter(
                    x=data['Datetime'], y=data['SMA 20'], name='SMA 20'))
            elif indicator == 'EMA 20':
                fig.add_trace(go.Scatter(
                    x=data['Datetime'], y=data['EMA 20'], name='EMA 20'))

        fig.update_layout(title=f"{ticker} {time_period.upper()} Chart",
                          xaxis_title='Time', yaxis_title='Price (USD)', height=600)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader('Historical Data')
        st.dataframe(
            data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])

        st.subheader('Technical Indicators')
        st.dataframe(data[['SMA 20', 'EMA 20']])

else:
    # --------------------------------------------------------------------------
    # MODE B: NEW STOCHASTIC STRATEGY BACKTEST ENGINE
    # --------------------------------------------------------------------------
    st.subheader("Stochastic Strategy Validation Engine")
    st.markdown(
        "Stress-testing the baseline **SMA-20/EMA-20** trend crossover logic across thousands of "
        "synthetic market lifetimes generated via **Geometric Brownian Motion (GBM)**."
    )

    # Render customized parameter control widgets in the sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("Monte Carlo Parameters")
    n_paths = st.sidebar.slider(
        "Simulation Paths (N)", min_value=100, max_value=2000, value=500, step=100)
    volatility = st.sidebar.slider(
        "Asset Volatility (σ)", min_value=0.05, max_value=0.60, value=0.25, step=0.05)
    drift = st.sidebar.slider("Expected Annual Drift (μ)",
                              min_value=-0.20, max_value=0.20, value=0.05, step=0.01)

    if st.sidebar.button('Run Stress Test'):
        with st.spinner("Executing vectorized parallel simulation paths..."):
            # 1. Generate paths via math module
            # Initial stock price fixed at 100, Horizon = 1 year (252 trading days)
            raw_paths = generate_gbm_paths(
                S0=100, mu=drift, sigma=volatility, T=1.0, dt=1/252, n_paths=n_paths)

            # 2. Backtest crossover strategy across all generated matrix arrays simultaneously
            sharpes, drawdowns, final_returns = run_vectorized_backtest(
                raw_paths, fast_window=20, slow_window=50)

        # Display aggregate macro performance metrics panels
        st.write("### Strategy Performance Aggregates")
        m1, m2, m3 = st.columns(3)
        m1.metric("Expected Annualized Sharpe", f"{np.mean(sharpes):.2f}")
        m2.metric("Median Maximum Drawdown",
                  f"{np.median(drawdowns) * 100:.2f}%")
        m3.metric("Probability of Positive Alpha",
                  f"{np.mean(final_returns > 0) * 100:.1f}%")

        # Plot distribution curves using Plotly Express (matching your dashboard theme)
        st.write("---")
        st.write("### Strategy Risk Profile Distributions")

        df_metrics = pd.DataFrame({
            "Sharpe Ratio": sharpes,
            "Max Drawdown (MDD)": drawdowns * 100
        })

        # Chart 1: Sharpe Ratio Histogram
        fig_sharpe = px.histogram(
            df_metrics, x="Sharpe Ratio", nbins=40,
            title="Probability Density Function: Strategy Sharpe Ratios",
            color_discrete_sequence=['#636EFA']
        )
        fig_sharpe.update_layout(
            xaxis_title="Sharpe Ratio Index", yaxis_title="Frequency Dynamic Count")
        st.plotly_chart(fig_sharpe, use_container_width=True)

        # Chart 2: Drawdown Histogram
        fig_mdd = px.histogram(
            df_metrics, x="Max Drawdown (MDD)", nbins=40,
            title="Distribution Profile: Maximum Strategy Portfolio Peak-to-Trough Drawdowns",
            color_discrete_sequence=['#EF553B']
        )
        fig_mdd.update_layout(xaxis_title="Maximum Drawdown (%)",
                              yaxis_title="Frequency Dynamic Count")
        st.plotly_chart(fig_mdd, use_container_width=True)
