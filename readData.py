# -*- coding: utf-8 -*-
"""
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
from sklearn.decomposition import PCA

def readData(param, if_debug):
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
        rebal = period*22 # assuming 22 trading days in a month
    elif unit=="D":
        rebal = period
    else:
        raise Exception("please input a vaild rebalance period...")
    # sort datetime index in ascending order
    xls       = pd.ExcelFile(fileName)
    df        = pd.read_excel(xls,'Price',index_col=0).sort_index()
    rets      = df.pct_change().fillna(0)
    secnames  = df.columns.to_numpy()
    nAssets   = len(secnames)
    dates     = df.index.to_numpy()
    if param['PortConstr'] == "bl":
        # black litterman model needs market cap data
        mktCap = pd.read_excel(xls,'Cap',index_col=0).sort_index()
        
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
    pca = PCA(n_components=2) # selecting top 2 vectors
    for loc in range(rebal,len(dates)):
        # Always use pca to reduce noise in cov matrix
        pca.fit(rets.iloc[loc-rebal:loc])
        cov = pca.get_covariance()
        COV[dates[loc]] = cov
        if param['PortConstr'] in ("equal","equalvol"):
            # euqal and equalvol portfolio do not need expected returns
            er = np.zeros(nAssets)
        elif param['PortConstr'] == "bl":
            # Black litterman expected return
            # using momentum Views for now
            # expected return formular 
            #    ER = [(scalar*cov)^(-1)+P.T*bigSig^-1*P]*[(scalar*cov)^(-1)+P.T*bigSig^-1*Q]
            #    scalar: user defined weights between market weights and model weights
            #    cov: covariance matrix
            #    P: identification matrix for assets and views
            #    Q: manager views(use momentum view for now)
            #    bigSig: confidence matrix for each views
            # NOTE: For manager's view matrix Q it can be both
            #       absolute view and relative view
            scalar = 5
            numView = 1
            curCap = (mktCap.iloc[loc]/sum(mktCap.iloc[loc])).to_numpy()
            # I use single relative momentum views for now
            # assume the view are winning stock outperform
            # lossing stock by 10% in the next period
            Q  = 10*np.ones((numView,1))
            cur_p = df.iloc[loc]
            pre_p = df.iloc[loc-rebal]
            period_ret = sorted([[ind,ret] for ind,ret in enumerate((cur_p-pre_p)/pre_p)],key=lambda x:x[1])
            P = np.ones((numView,nAssets))
            # assign views into P matrix
            # note here assume numView is only 1
            for i in range(len(period_ret)//2):
                ele = period_ret[i]
                P[0][ele[0]]=-1
            if len(period_ret)%2!=0:
                P[0][len(period_ret)//2+1]=0
            # bigSig is the uncertainty in each views
            bigSigInv = np.linalg.inv(np.dot(P,np.dot(cov,P.T)))
            covSaInv = np.linalg.inv(scalar*cov)
            part1 = np.linalg.inv(covSaInv+np.dot(P.T,np.dot(bigSigInv,P)))
            part2 = np.dot(covSaInv,curCap.T)+np.dot(P.T,np.dot(bigSigInv,Q)).T
            er = np.dot(part1,part2.T).T
        elif param['PortConstr'] == "mv":
            er = stats.gmean(1+rets.iloc[loc-rebal:loc],axis=0)-1
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
    # it is crucial to have a better expected return
    # and cov matrix I provide a data debugging here
    # to show the changes along time of expected
    # returns vectors
    if if_debug:
        # plot expected returns series
        print("Expected returns debug plot...")
        er_li = []
        for dd,vals in ER.items():
            temp = {"Dates": dd}
            for v,nm in zip(vals,secnames):
                if nm not in temp:
                    temp[nm] = v
            er_li.append(temp)
        df = pd.DataFrame.from_records(er_li).set_index("Dates")
        df.plot()
    return ret_dict


