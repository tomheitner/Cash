import requests
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

def second_derivative(x, fs=1, filt_smooth=1):
    lap_filt = np.repeat([1,  -2, 1], repeats=filt_smooth)/filt_smooth
    x_dotaim = correlate(x, lap_filt, mode='valid')
    
    # to account for sampling
    factor = (fs/(2*np.pi))**2
    x_dotaim *= factor
    
    # the end index for the time axis
    stop_ix = len(x) - len(lap_filt) + 1
    
    return stop_ix, x_dotaim


def derivative(x, fs=1, filt_smooth=1):
    der_filt = np.repeat([-1, 1], repeats=filt_smooth)/filt_smooth
    x_dot = correlate(x, der_filt, mode='valid')

    # to account for sampling
    factor = fs/(2*np.pi)
    x_dot *= factor
    
    # the end index for the time axis
    stop_ix = len(x) - len(der_filt) + 1 
    
    return stop_ix, x_dot


def moving_avg(x, how_much=5):
    filt = np.ones(how_much)/how_much
    x_smooth = correlate(x, filt, mode='valid')
    
    return x_smooth
# def should_buy(price_array):
    