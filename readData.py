# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:33:07 2020
This funtion reads data from csv file or
local database after user setting up.
readData funtion will look
    in the current directory of
    fileName.xlsx file of data
    return data structure is a dict
    dict = {
          "secnames":np.array, assets names
          "Rets":np.matrix, daily returns
          "dates":np.array, trading days
          "COV":dict of [date:np.matrix], cov matrix
          "ER":np.matrix, expected returns
          "rebaldates": np.array, rebalance dates
         }
NOTE: make sure you are supplying it with DAILY dataset
      the dataset should be stored in the first sheet
      also the first column in the sheet should be datetime
      the first row in the sheet should has security's name
@author: Shaolun Du
@contact: shaolun.du@gmail.com
"""
import pandas as pd
import numpy as np
from scipy import stats
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
    df        = pd.read_excel(fileName, index_col=0).sort_index()
    rets      = df.pct_change().fillna(0)
    secnames  = df.columns.to_numpy()
    nAssets   = len(secnames)
    dates     = df.index.to_numpy()
    # skip the first rebalance date
    # because we need to calculate historical return and cov
    # always shift rebalance date by one since we start on day0
    rebaldates= [dates[i*rebal+1] for i in range(1,len(dates)//rebal)]
    # always addin the last trading date
    if dates[-1] not in rebaldates:
        rebaldates.append(dates[-1])
    rebaldates = np.array(rebaldates)
    ER = {}
    COV = {}
    for loc in range(rebal,len(dates)):
        cov = rets.iloc[loc-rebal:loc].cov()
        COV[dates[loc]] = cov
        if param['ERmethod']=="hist":
            # epected return based on historical average
            er = stats.gmean(1+rets.iloc[loc-rebal:loc],axis=0)-1
        elif param['ERmethod']=="mom":
            # momentum expected return
            er = np.zeros(len(secnames))
        elif param['ERmethod']=="bl":
            # black litterman expected return
            er = np.zeros(len(secnames))
        ER[dates[loc]] = er
        
    # return dictionary setup
    ret_dict = {}
    ret_dict["secnames"]   = secnames
    ret_dict["rets"]       = rets[rebal:]
    ret_dict["dates"]      = dates[rebal:]
    ret_dict["COV"]        = COV
    ret_dict["ER"]         = ER
    ret_dict["rebaldates"] = rebaldates
    ret_dict["nAssets"]    = nAssets
    return ret_dict


