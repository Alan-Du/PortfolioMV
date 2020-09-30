# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 09:49:13 2020

This function perform a backtest of portfolio of risky securities.
The portfolio can be constructed in several different ways:
(1) Equal weighting (equal)
(2) Equal vol-weighting (equalvol)
(3) Mean-Variance optimization (mv)
(4) black litterman optimization (bl)

Inputs: 
    param - structure that specifies the backtest to run
    Data  - dataset (factor returns and covariances, security names, and
            rebalancing dates)
Outputs:
    output_struct - structure with extensive outputs
Notes:
1. We assume the first portfolio is all in cash
2. Portfolio weights are stored in their cash allocation (dollars) and indexed such that W(t) align with Rets(t):
(a) Rets(t) corresponds to the security return over the time period (t-1,t]
(b) W(t) corresponds to the portfolio weights held over the time period (t-1,t]
3. The value of the portfolio is calculated at the end of each time
period. In other words, if the time period is (t-1,t] the portfolio value
is calculated at time t.

@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
import numpy as np
from cvxopt.solvers import qp

def backTest(param, Data, if_debug):
    # read info from Dataset
    secnames   = Data['secnames']
    rets       = Data['rets']
    dates      = Data['dates']
    COV        = Data['COV']
    ER         = Data['ER']
    rebaldates = Data['rebaldates']
    nAssets    = Data['nAssets']
    # Define variables and allocate space
    T              = len(dates)
    cash           = np.zeros(T)
    tcosts         = np.zeros(T)
    turnover       = np.zeros(T)
    portVal        = np.zeros(T)
    portRet        = np.zeros(T)
    retdates       = np.zeros(T)
    W              = np.zeros((nAssets,T))
    RiskContr      = np.zeros((nAssets,T))
    securityRet    = np.zeros((nAssets,T))
    RiskProj       = np.zeros(T)
    SigStale       = np.zeros((nAssets,nAssets))
    cash[0]        = param['capital']
    portVal[0]     = cash[0]
    portValCurrent = portVal[0]
    wCurrent       = W[:,0]
    # Now move forward in time and rebalalance when needed
    for t in range(1,T):
        date_t = dates[t]
        if if_debug:
            print("Current Time:{}".format(date_t))
            print("Current weights:{}".format(wCurrent))
        # Covariance matrix 
        Sig = COV[date_t]
        mu  = ER[date_t]
        # Determine if we need to rebalance
        if_rebal = True if date_t in rebaldates else False
        if if_rebal:  # We need to rebalance
            if if_debug:
                print('Rebalancing...')
            SigStale = Sig
            if param['PortConstr'] == 'equal':
                wNew = portValCurrent*(np.ones(nAssets)/nAssets)
            if param['PortConstr'] == 'equalvol':
                vols       = np.sqrt(np.diagonal(Sig))
                volsinv    = 1/vols
                volsinvsum = sum(volsinv)
                wNew       = portValCurrent*(volsinv/volsinvsum)
            if param['PortConstr'] == 'mv':
                # Here lambda stands for 2*lambda
                # Long-short weights
                lambda2 = 8
                wNew    = portValCurrent*qp(Sig*lambda2,-mu,[],[],np.ones((1,len(Sig))),1)['x']
            if param['PortConstr'] == 'bl':
                # to be implemented...
                wNew = wCurrent
        else:
            # We don't need to rebalance
            wNew = wCurrent
        wTsigw           = np.dot(np.dot(wNew,Sig),wNew)
        wTsigwStale      = np.dot(np.dot(wNew,SigStale),wNew)
        W[:,t]           = wNew
        RiskProj[t]      = np.sqrt(wTsigw)/sum(wNew)
        RiskContr[:,t]   = np.dot(wNew,np.dot(Sig,wNew))/wTsigwStale
        trades           = wNew - wCurrent
        turnover[t]      = sum(abs(trades))/portValCurrent
        # Calculate portfolio at the end of the period
        # (If needed in the futute, add cash position here)
        wCurrent         = np.multiply(wNew,np.ones(nAssets)+rets.iloc[t].to_numpy())
        securityRet[:,t] = np.dot(wNew,rets.iloc[t].to_numpy().T)
        portValCurrent   = sum(wCurrent)
        portVal[t]       = portValCurrent
        portRet[t]       = (portVal[t]-portVal[t-1])/portVal[t-1]
        retdates[t]      = date_t
        # Error checking if current port value below zero
        if portVal[t]<0:
            raise Exception('Port val less than zero!{}\n'.format(portVal[t]))
        
    
    # Populate output structure
    output_struct                  = {}
    output_struct['portVal']       = portVal
    output_struct['dates']         = dates
    output_struct['W']             = W
    output_struct['RiskContrProj'] = RiskContr
    output_struct['RiskProj']      = RiskProj
    output_struct['cash']          = cash
    output_struct['turnover']      = turnover
    output_struct['secnames']      = secnames
    output_struct['securityRet']   = securityRet
    output_struct['portRet']       = portRet
    output_struct['retdates']      = retdates    
    output_struct['PortConstr']    = param['PortConstr']  
    return output_struct
