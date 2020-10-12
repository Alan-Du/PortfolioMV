# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 03:10:02 2020
Classifier on SP500 index based on below catogries:
    1. 1=short,2=short-non,3=non,4=long-non,5=long
This scripts using neural network algorithm to classify
stock market based on inter-market signals.
@author: Shaolun Du
@contact: shaolun.du@gmial.com
"""
# Data loading
%matplotlib inline
import pandas as pd
import numpy as np
import datetime as dt
import math
from scipy.signal import savgol_filter
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
# Global variable declaration
_r_f = 0.02 # rsik free rate
_day_year = 252 # trading days in a year
rets = lambda x: (x[-1] - x[0]) / x[0]
diffs = lambda x: x[-1] - x[0]
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
# plotting helper function
def _compare_plot(data,name1,name2):
    x = data.index
    y1 = data[name1]
    y2 = data[name2]
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(x, y1, 'g-')
    ax2.plot(x, y2, 'b-')
    ax1.set_xlabel('X data')
    ax1.set_ylabel(name1, color='g')
    ax2.set_ylabel(name2, color='b')
    plt.show()
    return fig