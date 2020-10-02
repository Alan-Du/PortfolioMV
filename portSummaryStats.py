# -*- coding: utf-8 -*-
"""
This function produces portfolio summary statistics
@author: Shaolun Du
@contact: shaolun.du@gmail.com
"""
import numpy as np
from maxDrawDown import maxDrawDown
from scipy.stats import kurtosis, skew

def portSummaryStats( output_struct, 
                      start_idx, end_idx, 
                      freq):
    summary_stats = {} # return dictionary
    
    portRet = output_struct['portRet']
    portVal = output_struct['portVal']
    retdates = output_struct['retdates']
    
    # Index and dates
    summary_stats['start_idx'] = start_idx
    summary_stats['end_idx'] = end_idx
    summary_stats['startdate'] = retdates[start_idx]
    summary_stats['enddate'] = retdates[end_idx-1]
    
    portRet = portRet[start_idx:end_idx]
    
    # Annualized return, vol, and Sharpe
    summary_stats['ann_ret'] = np.mean(portRet)*freq*100
    summary_stats['ann_vol'] = np.std(portRet)*np.sqrt(freq)*100
    summary_stats['ann_Sharpe'] = np.mean(portRet)/np.std(portRet)*np.sqrt(freq)
    
    # Skew and kurtosis
    summary_stats['skew'] = skew(portRet)
    summary_stats['kurtosis'] = kurtosis(portRet)
    
    # Max drawdown
    drawdown = maxDrawDown(portVal[start_idx:end_idx])
    summary_stats['drawdown'] = drawdown
    
    return summary_stats