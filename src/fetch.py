import streamlit as st  # for web app
import pandas as pd  # data manipulation
import yfinance as yf  # fetching financial data
import plotly.graph_objects as go  # visualizations
import plotly.express as px  # visualizations
from datetime import datetime, timedelta  # date and time manipulation
import pytz  # time zone handling
import ta  # technical analysis indicators

## part 1: function for pulling, processing and creating technical indicators##

# fetch data from yfinance, based on the ticker, period, and interval


def fetch_data(ticker, period, interval):
    end_date = datetime.now()
    if period == '1wk':
        start_date = end_date - timedelta(days=7)
        data = yf.download(ticker, start=start_date,
                           end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)
    return data


def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize(pytz.UTC)
    data.index = data.index.tz_convert('America/New_York')
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime;'}, inplace=True)
    return data
