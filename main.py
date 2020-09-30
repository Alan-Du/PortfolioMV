# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 13:56:16 2020

This script that calls the BackTest 
function to perform backtests of
portfolios of securities.

@author: Shaolun Du
@contact: shaolun.du@gmial.com
"""
import time
from readData import readData
from backTest import backTest
from portSummaryStatsAll import portSummaryStatsAll
from generateReport import generateReport

# Start clock
start = time.time()

# Degugging?
if_debug = False  # turn off debugging output
#if_debug = True  # turn on degugging output

# Data
param = {}
param['datasource'] = 'Data'
param['rebalFreq']  = "1M"   # rebal frequency could be nD(n days),nM(n months)
param['ERmethod']   = "hist"

# Read data here
Data = readData(param)

# General backtest parameters
param['freq']            = 260  # All data is daily, assuming 260 days in a year
param['capital']         = 10**6  # initial cash position in dollars
param['output_filename'] = [param['datasource']+'_output']

"""
param-PortConstr could be...
    1.equal: equal weighted portfolio
    2.equalvol: equal volatility portfolio
    3.mv: mean variance portfolio
    4.bl: black litterman portfolio
"""

# Backtesting
param['PortConstr']  = 'equalvol'
outputBackTest       = backTest(param,Data,if_debug)
summary              = portSummaryStatsAll(outputBackTest,param)
outputBackTest['smy']= summary

# report generation
generateReport(outputBackTest)

# Stop clock
end = time.time()
print("Total time passed:{}".format(end-start))    