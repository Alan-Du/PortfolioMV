# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:33:07 2020
This funtion reads data from csv file or
local database after user setting up.
@author: Shaolun Du
@contact: shaolun.du@gmail.com
"""

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
    #       "ER": np.matrix, expected returns
    #       "rebaldates": np.array, rebalance dates
    #   }
    fileName  = param['datasource']
    rebalFreq = param['rebalFreq']
    
    return None