from modules.tools.pattern_detection import is_hammer, is_bullish_engulfing

def bullish_reversal(
    df_data,
    bull_rev_patterns = [is_hammer, is_bullish_engulfing],
    max_bull_without_pattern = 3,
    min_bull_confirmation = 1,
    verbose = 0,
):
    '''
    Gets a Pandas DataFrame with OHLC data and returns whether the last few candlesticks indicate a bullish reversal (down to up).
    
    Input:
        df_data (pd.DataFrame) - OHLC data.
        bullish_patterns (list of functions) - a list of functions looking for patterns indicating bullish reversal
        max_bull_without_pattern (int) - maximal number of "confirmation" candles without a pattern indicating a bullish reversal
        min_bull_confirmation (int) - minimal number of bullish "confirmation" candles
        verbose (int) - to print, or not to print
        
    Returns:
        bull (boolean) - A boolean indicator, telling whether there has just now been a bullish reversal.
    '''
    
    # # we go in reverse chronological order, starting with the most recent candlestick
    # df_data_rev = df_data.iloc[::-1]
    
    
    if verbose > 0: print('Confirmation:')
    
    # =============================================================================
    # =========================== CONFIRMATION ====================================
    # =============================================================================
    
    # first we check for confirmation - is the most recent candlestick bullish?
    for i in range(1, min_bull_confirmation+1):
        last_candle = df_data.iloc[-i]
        if last_candle['Close'] < last_candle['Open']: 
            if verbose > 0: print('Most recent candle bearish - quitting')
            return False

    # =============================================================================
    # =========================== CONFIRMATION ====================================
    # =============================================================================
    if verbose > 0:
        print('V\n')
        print('Patterns:')
    # =============================================================================
    # ====================== LOOKING FOR PATTERNS =================================
    # =============================================================================
    '''
    goes from df_data[-2] to df_data[-max_bull-1]
    checks if those candles are bullish or a pattern indicaing a bullish reversal
    '''    
    for i in range(min_bull_confirmation, max_bull_without_pattern + min_bull_confirmation):  
        
        if verbose > 0: print('{} candle before confirmation'.format(i))
        
        '''
        we check if one of the known bullish reversal patterns happens in this spot
        this requires sending some past data, for now, we send all the past data
        '''
        data_check_pattern = df_data[:-i]  # from start to -i (including -i)
        is_bull_rev_pattern = False
        for func in bull_rev_patterns:
            is_bull_rev_pattern = is_bull_rev_pattern or func(data_check_pattern)
            
            # if we found one, no need to search further
            if is_bull_rev_pattern: 
                if verbose > 0: print('Pattern {} found!'.format(func.__name__))
                return True 
        
        if verbose > 0: print('No pattern')
        
        '''
        if no pattern was found we insist this candle must be bullish
        '''
        cur_candle = df_data.iloc[-i-1]
        is_bull = cur_candle['Close'] - cur_candle['Open'] > 0
        
        
        if not is_bull: 
            if verbose > 0: print("Isn't a bull - return False")
            return False
        if verbose > 0: print('Is bullish - continue'.format(i-1))
    
    # =============================================================================
    # ====================== LOOKING FOR PATTERNS =================================
    # =============================================================================
    
    if verbose > 0: print('No Patterns - Returning False')
    
    '''
    If we reached this point, no pattern was detected on the last <max_bull_without_pattern>, so we return False
    '''
    return False

    
def bearish_reversal(
    df_data,
    bull_rev_patterns = [is_hammer, is_bullish_engulfing],
    max_bear_without_pattern = 3,
    min_bear_confirmation = 1,
    verbose = 0,
):
    '''
    Gets a Pandas DataFrame with OHLC data and returns whether the last few candlesticks indicate a bearish reversal (up to down).
    
    Input:
        df_data (pd.DataFrame) - OHLC data.
        bullish_patterns (list of functions) - a list of functions looking for patterns indicating bullish reversal
        max_bull_without_pattern (int) - maximal number of "confirmation" candles without a pattern indicating a bullish reversal
        min_bull_confirmation (int) - minimal number of bullish "confirmation" candles
        verbose (int) - to print, or not to print
        
    Returns:
        bear (boolean) - A boolean indicator, telling whether there has just now been a bullish reversal.
    '''
    
    # the lazy way
    
    bear = bullish_reversal(
        df_data=-df_data,  # puts a - sign in front of all the the numeric values
        bull_rev_patterns = bull_rev_patterns,
        max_bull_without_pattern = max_bear_without_pattern,
        min_bull_confirmation = min_bear_confirmation,
        verbose = verbose,
    )
    
    return bear