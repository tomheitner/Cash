import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
import yfinance as yf

def pull_stock(
    symbol,
    interval = '1d', # Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
    start_year=None,
    start_month=None,
    start_day=None,
    end_year=None,
    end_month=None,
    end_day=None
):
    if end_year is None or end_month is None or end_day is None:
        end_date = datetime.now()  # default end date is now
    else:
        end_date = datetime(year=end_year, month=end_month, day=end_day)

    if start_year is None or start_month is None or start_day is None:
        start_date = end_date - timedelta(days=10)  # default start time is 10 days before end date
    else:
        start_date = datetime(year=start_year, month=start_month, day=start_day)

    data = yf.download(tickers=symbol, start=start_date, end=end_date, interval=interval)
    
    return data

def process_df(df_data):
    open_array = []
    hi_array = []
    low_array = []
    close_array = []
    time_axis = []

    for row_ix in range(len(df_data)):
        row = df_data.iloc[row_ix]
        row_time = datetime.strptime(row.name, '%Y-%m-%d %H:%M:%S')
        time_axis.append(row_time)
        open_array.append(float(row["1. open"]))
        hi_array.append(float(row["2. high"]))
        low_array.append(float(row["3. low"]))
        close_array.append(float(row["4. close"]))
        stock = {
            'open': open_array,
            'close': close_array,
            'high': hi_array,
            'low': low_array
        }
    return stock, time_axis

def plot_stock(df_data, symbol='', interval=None):
    
    stock, time_axis = process_df(df_data)
    
    x_size = 15
    y_size = 2

    title = ''
    if symbol is not None: title += 'Symbol: ' + symbol
    if interval is not None: title += '\nInterval: {}min'.format(interval)
    
    open_array = stock['open']
    hi_array = stock['high']
    low_array = stock['low']
    close_array = stock['close']
    
    y_max_val = np.max((open_array, hi_array, low_array, close_array))
    y_min_val = np.min((open_array, hi_array, low_array, close_array))

    plt.figure(figsize=(x_size, y_size))
    plt.plot(time_axis, open_array)
    plt.ylim(y_min_val, y_max_val)
    plt.title('Open\n' + title)
    plt.grid()
    plt.show()

    plt.figure(figsize=(x_size, y_size))
    plt.plot(time_axis, hi_array)
    plt.ylim(y_min_val, y_max_val)
    plt.title('High\n' + title)
    plt.grid()
    plt.show()

    plt.figure(figsize=(x_size, y_size))
    plt.plot(time_axis, low_array)
    plt.ylim(y_min_val, y_max_val)
    plt.title('Low\n' + title)
    plt.grid()
    plt.show()

    plt.figure(figsize=(x_size, y_size))
    plt.plot(time_axis, close_array)
    plt.ylim(y_min_val, y_max_val)
    plt.title('Close\n' + title)
    plt.grid()
    plt.show()