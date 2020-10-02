# -*- coding: utf-8 -*-
"""
This is the main function port to
call readData.py and backTest.py
performing portfolio backtesting
currently I implemented some simple
construction method listed below.
Please read readData.py first before change anything.
The input file should be an excel with pre-specified 
format. 
Dataset should contain at least price data.
If want to run black litterman model then
additonal data of market capital values of each secturity
should be provided in a sepreate data sheet.
Backtest.py is responsible for calcualte portfolio
value and weights at each rebalance date.
The backtest output will be auto-generated into output folder
in ".png" format, which includes 
    1. Summary table of stats of backtesting
    2. Plot of portVal vs rets and volatility
    3. Plot of portSharpe, MDD, weights, turnover

***If you find this is interesing or any bugs
please contact Shaolun Du directly

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
if_debug = False

"""
param-PortConstr could be...
    1.equal: equal weighted portfolio
    2.equalvol: equal volatility portfolio
    3.mv: mean variance portfolio
    4.bl: black litterman portfolio
"""

param = {}
param['datasource'] = 'Data'
param['rebalFreq']  = "3M"   # rebal frequency could be nD(n days),nM(n months)
param['PortConstr'] = 'bl'

# General backtest parameters
param['freq']            = 260  # All data is daily, assuming 260 days in a year
param['capital']         = 10**6  # initial cash position in dollars
param['output_filename'] = param['PortConstr']+param['rebalFreq']+'BacktestDetails'

# Read data here
Data = readData(param,if_debug)

# Backtesting
outputBackTest       = backTest(param,Data,if_debug)
summary              = portSummaryStatsAll(outputBackTest,param)
outputBackTest['smy']= summary

# report generation
generateReport(outputBackTest, param)

# Stop clock
end = time.time()
print("Total time passed:{}".format(end-start))    