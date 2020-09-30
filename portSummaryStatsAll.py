# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:28:44 2020
This function generates all portfolio summary stats
@author: Shaolun du
@contact: shaolun.du@gmail.co
"""
from portSummaryStats import portSummaryStats
import pandas as pd
def portSummaryStatsAll(output_struct,param):
    nDays = len(output_struct['retdates'])
    freq = param['freq']
    PortConstr = param['PortConstr']
    
    # Since inception
    summary = portSummaryStats(output_struct,1, nDays, freq)
    incep = [summary['ann_ret'], summary['ann_vol'], summary['ann_Sharpe'],
             summary['skew'], summary['kurtosis'], summary['drawdown'],'incep' ]
    # Last 5 years
    summary = portSummaryStats(output_struct,nDays-5*freq+1,nDays, freq)
    fiveYrs = [summary['ann_ret'], summary['ann_vol'], summary['ann_Sharpe'],
             summary['skew'], summary['kurtosis'], summary['drawdown'],'5year' ]
    # Last 3 years
    summary = portSummaryStats(output_struct,nDays-3*freq+1,nDays, freq)
    threeYrs = [summary['ann_ret'], summary['ann_vol'], summary['ann_Sharpe'],
             summary['skew'], summary['kurtosis'], summary['drawdown'],'3year' ]
    # Last 1 year
    summary = portSummaryStats(output_struct,nDays-  freq+1,nDays, freq)
    oneYr = [summary['ann_ret'], summary['ann_vol'], summary['ann_Sharpe'],
             summary['skew'], summary['kurtosis'], summary['drawdown'],'1year' ]
    
    ans = []
    for ele in [incep,fiveYrs,threeYrs,oneYr]:
        ans.append({
            'stra'  :PortConstr,
            'period':ele[6],
            'annRet':round(ele[0],3),
            'annVol':round(ele[1],3),
            'annShp':round(ele[2],3),
            'annSkw':round(ele[3],3),
            'annKrt':round(ele[4],3),
            'annMDD':round(ele[5],3),
            })
    return pd.DataFrame(ans).reset_index(drop=True)