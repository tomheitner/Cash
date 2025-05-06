import pandas as pd
import numpy as np
from modules.tools.sequence_detection import is_bear

eps = 1e-5  # to ensure we don't divide in zero

def is_hammer(
    df_data,
    hammer_strength_th = 1.2,  # required ratio between lower shadow and the rest of the candle
    check_for=3, 
):
    '''
    bullish reversal indicator
    
    A hammer isn't necesarily bullish or bearish, therefore a doji can be a legitimate hammer.
    A hammer must come in the context of a bearish trend.
    '''
    
    # confirm the last <check_for> candles that came before the last one are bearish.
    data_check_for_bear = df_data[-check_for-1:-1]
    bear_trend = is_bear(data_check_for_bear, check_for=check_for)
    
    # without a bear trend this isn't a true hammer!
    if not bear_trend: return False
    
    candle = df_data.iloc[-1]
    
    open_data = candle['Open']
    close_data = candle['Close']
    high_data = candle['High']
    low_data = candle['Low']
    
    body = np.abs(open_data - close_data)
    
    body_min = min(open_data, close_data)
    body_max = max(open_data, close_data)
    
    upper_shadow = high_data - body_max
    lower_shadow = body_min - low_data
        
    hammer_strength = lower_shadow / (body + upper_shadow + eps)
    
    return hammer_strength > hammer_strength_th



def is_bullish_engulfing(
    df_data,
    enforce_bear = False,
):
    '''
    bullish reversal indicator
    
    Check if the last candle is a bullish engulfing pattern, i.e. if the candle that came before was bearish, and this one is bullish 
    and has a close bigger than the previous high.
    
    Input:
        df_data (pd.DataFrame) - OHLC data
        enforce_bear (boolean) - indicates if we insist on the last one being bearish. If false, we just check for engulfment
    
    Returns:
        is_bull_eng (boolean) - is the last candle in a bullish engulfing pattern
    '''

    curr_candle = df_data.iloc[-1]
    prev_candle = df_data.iloc[-2]
    
    # if we require the previous candle is a bear, and it isn't, return False
    if enforce_bear and prev_candle['Close'] > prev_candle['Open']: return False
        
    # we require the current candle is bullish
    if curr_candle['Close'] < curr_candle['Open']: return False

    # now all that's left is to check if the current close engulfes the previous high
    return curr_candle['Close'] > prev_candle['High'] and curr_candle['Open'] < prev_candle['Close']