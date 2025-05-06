import pandas as pd
import numpy as np

# =========================================================================================================
# ========================================== NAIVE ========================================================
# =========================================================================================================

def is_bull_naive(
    df_data,
    check_for=5,
):
    '''
    Check if all the last <check_for> candles have been bullish.
    '''
    
    if check_for == 0: return True  # nothing to check

    # we go in reverse chronological order, starting with the most recent candlestick
    df_data_rev = df_data.iloc[::-1]
    
    # goes from df_data_rev[0] to df_data[check_for-1] and checks if those candles are bullish
    for i in range(check_for):  
        cur_candle = df_data_rev.iloc[i]
        is_bull = cur_candle['Close'] > cur_candle['Open']
        
        # it's a bearish candlestick!
        if not is_bull:  
            return False
    
    return True



def is_bear_naive(
    df_data,
    check_for=5,
):
    '''
    Check if all the last <check_for> candles have been bearish.
    '''
    
    if check_for == 0: return True  # nothing to check 
    
    # we go in reverse chronological order, starting with the most recent candlestick
    df_data_rev = df_data.iloc[::-1]
    
    # goes from df_data_rev[0] to df_data[check_for-1] and checks if those candles are bullish
    for i in range(check_for):  
        cur_candle = df_data_rev.iloc[i]
        is_bear = cur_candle['Close'] < cur_candle['Open']
        
        # it's a bullish candlestick!
        if not is_bear:  
            return False
    
    return True

# =========================================================================================================
# ========================================== NAIVE ========================================================
# =========================================================================================================


# =========================================================================================================
# ====================================== A LITTLE LESS NAIVE ==============================================
# =========================================================================================================

def is_bull(
    df_data,
    check_for=5,
):
    '''
    Check if most of the last <check_for> candles have been bullish and that the price has gone up.
    '''
    
    if check_for == 0: return True  # nothing to check 
    
    # first, we check if the overall the price has gone up
    first_open = df_data.iloc[-check_for]['Open']
    last_close = df_data.iloc[-1]['Close']
    
    # if price has gone down, not much of a bull
    if last_close < first_open: return False  
    
    # we go in reverse chronological order, starting with the most recent candlestick
    df_data_rev = df_data.iloc[::-1]
    
    # goes from df_data_rev[0] to df_data[check_for-1] and checks if there are more bears than bulls
    bulls = 0
    for i in range(check_for):  
        cur_candle = df_data_rev.iloc[i]
        bulls += 1 if cur_candle['Close'] > cur_candle['Open'] else -1

    return bulls > 0

def is_bear(
    df_data,
    check_for=5,
):
    '''
    Check if most of the last <check_for> candles have been bearish and that the price has gone down.
    '''
    
    if check_for == 0: return True  # nothing to check 
    
    # first, we check if the overall the price has gone down
    first_open = df_data.iloc[-check_for]['Open']
    last_close = df_data.iloc[-1]['Close']
    
    # if price has gone up, not much of a bear
    if last_close > first_open: return False  
    
    # we go in reverse chronological order, starting with the most recent candlestick
    df_data_rev = df_data.iloc[::-1]
    
    # goes from df_data_rev[0] to df_data[check_for-1] and checks if there are more bears than bulls
    bears = 0
    for i in range(check_for):  
        cur_candle = df_data_rev.iloc[i]
        bears += 1 if cur_candle['Close'] < cur_candle['Open'] else -1
    
    return bears > 0


# =========================================================================================================
# ====================================== A LITTLE LESS NAIVE ==============================================
# =========================================================================================================
