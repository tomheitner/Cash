import requests
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

# my lib
import modules.tools as tools
import modules.utils as utils
from modules.config import api_key



def simulator(x, fs, lookback, buy_func, buy_params, sell_func, sell_params):

    # for plots
    buys = []
    sells = []
    
    keren = np.mean(x)
    kesef = keren
    has_bought = False
    for time_ix in range(lookback, len(x)):
        x_as_of_now = x[:time_ix]  # simulates the signal until now
        cur_val = x_as_of_now[-1]
        
        # buy
        if not has_bought and buy_func(x_as_of_now, **buy_params):
            kesef -= cur_val
            val_buy = cur_val
            buys.append(time_ix)
            has_bought = True
            continue
        
        # sell        
        # if has_bought and sell_func(x_as_of_now, **sell_params):
        if has_bought and cur_val > val_buy and sell_func(x_as_of_now, **sell_params):
            kesef += cur_val
            sells.append(time_ix)
            has_bought = False
            
    
    # simulation ends, if still holding, sell
    if has_bought:
        kesef += x[-1]
    
    t = np.arange(len(x))

    
    plt.figure(figsize=(10, 5))
    plt.plot(t, x)
    if len(buys)>0: plt.plot(t[buys], x[buys], linestyle='None', marker='^', c='Green')
    if len(sells)>0: plt.plot(t[sells], x[sells], linestyle='None', marker='v', c='Red')
    
    print('Keren: {}'.format(keren))
    print('kesef: {}'.format(kesef))
    tsua = 100*(kesef-keren)/keren
    print('Tsua: {}%'.format(tsua))

    
    return buys, sells