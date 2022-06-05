import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def value_time_series(strategy1, label1, strategy2, label2, strategy3, label3):
    value_fig, value_ax = plt.subplots()
    value_ax.plot(strategy1.index, strategy1['Portfolio Value'], label= label1 + ' Portfolio Value')
    value_ax.plot(strategy2.index, strategy2['Portfolio Value'], label= label2 + ' Portfolio Value')
    value_ax.plot(strategy3.index, strategy3['Portfolio Value'], label=label3 + ' Portfolio Value')
    value_ax.legend()
    value_ax.set_xlabel('Year')  # Need to double check how currencies work in Yfinance
    value_ax.set_ylabel("Value")
    value_ax.set_title("Net Asset Value over Time")
    value_ax.xaxis.set_major_formatter(mdates.DateFormatter('%yy'))

    return value_fig

def cash_time_series(strategy1, label1, strategy2, label2, strategy3, label3):
    cash_fig, cash_ax = plt.subplots()
    cash_ax.plot(strategy1.index, strategy1['Cash'], label= label1 + ' Cash Amount')
    cash_ax.plot(strategy2.index, strategy2['Cash'], label=label2 + ' Cash Amount')
    cash_ax.plot(strategy3.index, strategy3['Cash'], label=label3 + ' Cash Amount')
    cash_ax.legend()
    cash_ax.set_xlabel('Year')  # Need to double check how currencies work in Yfinance
    cash_ax.set_ylabel("Value")
    cash_ax.set_title("Cash Account over Time")
    cash_ax.xaxis.set_major_formatter(mdates.DateFormatter('%yy'))
    return cash_fig