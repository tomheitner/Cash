import requests
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from modules.config import api_key

def pull_stock(symbol, interval=1, show_plots=False, return_df=False):
    df_data = make_request(symbol, interval=interval)
    stock, time_axis = process_df(df_data)
    if show_plots: plot_stock(stock, time_axis, symbol=symbol, interval=interval)
    
    if return_df: 
        return stock, time_axis, df_data
    else:
        return stock, time_axis

def make_request(symbol, interval=1):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval={}min&apikey={}'.format(symbol, interval, api_key)
    r = requests.get(url)
    json_obj = r.json()

    data = json_obj['Time Series ({}min)'.format(interval)]
    # df_data = pd.DataFrame(pd.DataFrame(data).T, index=range(len(data)))
    df_data = pd.DataFrame(data).T
    return df_data

def format_df_for_backtest(df_data):
    df_data = df_data.rename(columns = {
        "1. open":'Open',
        "2. high":'High',
        "3. low":'Low',
        "4. close":'Close', 
        "5. volume":'Volume'
    }, inplace = False)
    return df_data

def pull_stock_for_backtest(symbol, interval=1):
    df_data = make_request(symbol, interval=interval)
    df_data = format_df_for_backtest(df_data)
    return df_data

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

def plot_stock(stock, time_axis, symbol='', interval=None):
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