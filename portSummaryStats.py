# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:46:10 2020
This function produces portfolio summary statistics
@author: Shaolun Du
@contact: shaolun.du@gmail.com
"""
import numpy as np
from maxdrawdown import maxdrawdown
from scipy.stats import kurtosis, skew
def portSummaryStats( output_struct, 
                      start_idx, end_idx, 
                      freq):
    summary_stats = {} # return dictionary
    
    portRet = output_struct['portRet']
    retdates = output_struct['retdates']
    
    # Index and dates
    summary_stats['start_idx'] = start_idx
    summary_stats['end_idx'] = end_idx
    summary_stats['startdate'] = retdates[start_idx] 
    summary_stats['enddate'] = retdates[end_idx]
    
    portRet = portRet[start_idx:end_idx]
    
    # Annualized return, vol, and Sharpe
    summary_stats['ann_ret'] = np.mean(portRet)*freq*100
    summary_stats['ann_vol'] = np.std(portRet)*np.sqrt(freq)*100
    summary_stats['ann_Sharpe'] = np.mean(portRet)/np.std(portRet)*np.sqrt(freq)
    
    # Skew and kurtosis
    summary_stats['skew'] = skew(portRet)
    summary_stats['kurtosis'] = kurtosis(portRet)
    
    # Max drawdown
    # to be implemented
    drawdown = maxdrawdown(portRet)
    summary_stats['drawdown'] = -drawdown*100
    
    return summary_stats