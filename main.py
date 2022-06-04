import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

#Set high level options
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns',10)

#Declare Variables
ticker_symbol = 'MSFT'
start_date = '2015-6-1' #American Dates
end_date = '2022-6-3' #American Dates
intervals = '1d'

#get ticker data
ticker_data = yf.Ticker(ticker_symbol)

#Get Historical Prices
ticker_df = ticker_data.history(period = intervals, start = start_date, end = end_date)

# Create the trading dataframe
trading_df = ticker_df[['Open', 'Close']]

#Simple Strategy, sell when close < open, and vice versa. No short Selling or debt allowed
trading_df["Previous Period Price Decrease"] = trading_df.Open.shift(1) - trading_df.Close.shift(1)

trading_df.loc[trading_df['Previous Period Price Decrease'] < 0, 'Transaction'] = 1
trading_df.loc[trading_df['Previous Period Price Decrease'] >= 0, 'Transaction'] = -1
trading_df.loc[pd.isna(trading_df['Previous Period Price Decrease']), 'Transaction'] = 0
trading_df['Number of Shares Owned'] = trading_df['Transaction'].cumsum()
trading_df.loc[trading_df['Transaction'] == 0, 'Cash'] = 10000 #Starting with 10000$
trading_df.loc[trading_df['Transaction'] != 0, 'Cash'] = -1 * trading_df['Transaction'] * trading_df['Close'] #Starting with 10000$
trading_df["Cash"] = trading_df['Cash'].cumsum()

# In performance analysis, we assume we get the close price when buying and selling
trading_df['Share Value'] = trading_df['Number of Shares Owned'] * trading_df['Close']
trading_df['Portfolio Value'] = trading_df['Cash'] + trading_df['Share Value']

# Graph Performance
plt.plot(trading_df.index,trading_df['Portfolio Value'])
plt.plot(trading_df.index, trading_df['Cash'])
plt.plot(trading_df.index, trading_df['Number of Shares Owned'])
plt.show()

print(trading_df.index)




