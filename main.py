import pandas as pd
import streamlit as st
from Projection_Functions import create_standard_account_values
from Strategies import control_function
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
col5, col6 = st.columns(2)

with col1:
    ticker = st.text_input('What Ticker would you like to use?', value = 'MSFT')

with col2:
    start, end = st.slider(
        'Date Range for the Analysis',
        value = (datetime(2015,1,1),datetime(2022,1,1))
                 ,format = 'MM/DD/YY'
    )

with col3:
    interval = st.selectbox('Interval of prices for analysis',
                          ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo'])

with  col4:
    cash = st.slider('Beginning Cash Value', 0, 1000000, 10000, format = "%f$")

with col5:
    strat1 = st.selectbox('Which Strategy are you simulating? (Strategy 1)',
                          ['buy_and_hold','simple_momentum'])
with col6:
    strat2 = st.selectbox('Which Strategy are you simulating? (Strategy 2)',
                          ['buy_and_hold','simple_momentum'])

#Declare Variables
ticker_symbol = ticker
start_date = start
end_date = end
intervals = interval
starting_cash = cash
strategy1 = strat1
strategy2 = strat2

# Create the main strategy
strategy1_df = control_function(strategy1, starting_cash, ticker_symbol, start_date, end_date, intervals)

# Calculate Account Values
strategy1_df = create_standard_account_values(strategy1_df, starting_cash)

# Same for second strategy
strategy2_df = control_function(strategy2, starting_cash, ticker_symbol, start_date, end_date, intervals)
strategy2_df = create_standard_account_values(strategy2_df, starting_cash)

# Buy the SP 500
control_sp_df = control_function('buy_and_hold_sp', starting_cash, ticker_symbol, start_date, end_date, intervals)
control_sp_df = create_standard_account_values(control_sp_df, starting_cash)

# Graph Performance
st.pyplot(value_time_series(strategy1_df, strat1, strategy2_df, strat2, control_sp_df, 'Buy and Hold SP'))
st.pyplot(cash_time_series(strategy1_df, strat1, strategy2_df, strat2, control_sp_df, 'Buy and Hold SP'))

st.write(strategy1_df)