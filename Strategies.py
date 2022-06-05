# This file contains the functions to describe the strategies

import streamlit as st
import yfinance as yf
import math

@st.cache(allow_output_mutation=True)
def import_price_data(ticker, start, end, trade_interval):
    ticker_data = yf.Ticker(ticker)
    return ticker_data.history(period = trade_interval, start = start, end = end)

def buy_and_hold(initial_cash, price_data_df):
    # Double check that all the required columns exist
    cols = price_data_df.columns
    if 'Close' not in cols:
        raise Exception('A Close value is required to calculate account values')
    if 'Open' not in cols:
        raise Exception('A Open value is required to calculate account values')

    # Initialise Transaction
    price_data_df['Transaction'] = 0

    # Get the column index
    transaction_index = price_data_df.columns.get_loc('Transaction')
    close_index = price_data_df.columns.get_loc('Close')

    # Buy as much as possible at day 1
    price_data_df.iloc[0, transaction_index] = math.floor(initial_cash / price_data_df.iloc[0, close_index])

    return price_data_df

def simple_momentum(price_data_df):
    # Double check that all the required columns exist
    cols = price_data_df.columns
    if 'Close' not in cols:
        raise Exception('A Close value is required to calculate account values')
    if 'Open' not in cols:
        raise Exception('A Open value is required to calculate account values')

    # Initialise Transaction
    price_data_df['Transaction'] = 0

    # Fill in Transaction
    price_data_df["Previous Period Price Decrease"] = price_data_df.Open.shift(1) - price_data_df.Close.shift(1)

    price_data_df.loc[price_data_df['Previous Period Price Decrease'] < 0, 'Transaction'] = 1
    price_data_df.loc[price_data_df['Previous Period Price Decrease'] >= 0, 'Transaction'] = -1

    return price_data_df