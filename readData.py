# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:33:07 2020
This funtion reads data from csv file or
local database after user setting up.
@author: Shaolun Du
@contact: shaolun.du@gmail.com
"""
import pandas as pd
from scipy.stats.mstats import gmean

def readData(param):
    # readData funtion will look
    # in the current directory of
    # fileName.xlsx file of data
    # return data structure is a dict
    # dict = {
    #       "secnames":np.array, assets names
    #       "Rets":np.matrix, daily returns
    #       "dates":np.array, trading days
    #       "COV":dict of [date:np.matrix], cov matrix
    #       "ER":np.matrix, expected returns
    #       "rebaldates": np.array, rebalance dates
    #   }
    ret_dict = {}
    fileName  = param['datasource']+".xlsx"
    rebalFreq = param['rebalFreq']
    period = int(rebalFreq[:-1])
    unit = rebalFreq[-1]
    if unit=="M":
        # assuming 22 trading days in a month
        rebal = period*22
    elif unit=="D":
        rebal = period
    else:
        raise Exception("please input a vaild rebalance period...")
        
    # sort datetime index in ascending order
    df = pd.read_excel(fileName, index_col=0).sort_index()
    Rets = df.pct_change()
    secnames = df.columns.to_numpy()
    dates = df.index.to_numpy()
    if param['ERmethod']=="hist":
        # epected return based on historical average
        ER = Rets.rolling(window=rebal).apply(gmean)
    if param['ERmethod']=="bl":
        # to be implemented
        ER = Rets.rolling(window=rebal).apply(gmean)
    
    return None


####
param = {"datasource":"Data",
         "rebalFreq":"1M"}
readData(param)