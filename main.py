import pandas as pd
import streamlit as st
from Projection_Functions import create_standard_account_values
from Strategies import buy_and_hold, import_price_data, simple_momentum
from graphing_functions import value_time_series, cash_time_series
from datetime import datetime

#Set high level options
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns',10)

# Add a sidebar to the App
st.sidebar.markdown('### A basic analysis of different trading strategies')
st.sidebar.markdown('The purpose of this app is to implement some basic trading strategies and provide some')

# Add a title to the app
st.title('Trading strategy Technical Analysis')

# Create some inputs for the user
col1, col2, col3, col4 = st.columns(4)

with col1:
    ticker = st.text_input('What Ticker would you like to use?', value = 'MSFT')

with col2:
    start, end = st.slider(
        'Date Range for the Analysis',
        value = (datetime(2015,1,1),datetime.today())
                 ,format = 'MM/DD/YY'
    )

with col3:
    interval = st.selectbox('Interval of prices for analysis',
                          ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo'])

with  col4:
    cash = st.slider('Beginning Cash Value', 0, 1000000, 10000, format = "%f$")

#Declare Variables
ticker_symbol = ticker
start_date = start
end_date = end
intervals = interval
starting_cash = cash

#get ticker data
ticker_data_df = import_price_data(ticker_symbol, start_date, end_date, intervals)

# Create the trading dataframe
trading_df = ticker_data_df[['Open','Close']]

#Simple Momentum Strategy, sell when close < open, and vice versa. No short Selling or debt allowed
trading_df = simple_momentum(trading_df)

# Projected Strategy
trading_df = create_standard_account_values(trading_df, starting_cash)

# What would happen if we just bought and hold this stock?
buy_and_hold_df = buy_and_hold(starting_cash,ticker_data_df)
buy_and_hold_df = create_standard_account_values(buy_and_hold_df, starting_cash)

# Graph Performance
st.pyplot(value_time_series(trading_df, 'Simple Momentum', buy_and_hold_df, 'Buy and Hold'))
st.pyplot(cash_time_series(trading_df, 'Simple Momentum', buy_and_hold_df, 'Buy and Hold'))

# Load in the Projection DF
st.write(trading_df[['Close','Transaction','Cash','Share Value']])
