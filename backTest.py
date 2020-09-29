# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 09:49:13 2020

This function perform a backtest of portfolio of risky securities.
The portfolio can be constructed in several different ways:
(1) Equal weighting (equal),
(2) Equal vol-weighting (equalvol),
(3) Mean-Variance optimization (mv)

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
def backTest(param, Data, if_debug):
    secnames = Data['secnames']
    Rets = Data['Rets']
    dates = Data['dates']
    COV = Data['COV']
    ER = Data['ER']
    rebaldates = Data['rebaldates']
    nAssets = Data['param_Data']['nAssets']
    
    # Define variables and allocate space
    T = len(dates)
    cash = np.zeros(T)
    tcosts = np.zeros(T)
    turnover = np.zeros(T)
    portVal = np.zeros(T)
    portRet = np.zeros(T-1)
    retdates = np.zeros(T-1)
    W = np.zeros(nAssets,T)
    RiskContr = np.zeros(nAssets,T-1)
    securityRet = np.zeros(nAssets)
    RiskProj = np.zeros(T-1)
    
    # At t = 1
    # Initial portfolio value
    # and risk factor allocations
    cash[0] = param['capital']
    portVal[0] = cash[0]
    
    portValCurrent = portVal[0]
    wCurrent = W[:,0]
    # Now move forward in time and rebalalance when needed
    for t in range(1,T):
        if if_debug:
            print(t)
        # Covariance matrix 
        Sig = COV[:,:,t]
        mu = ER[:,t]
        # Determine if we need to rebalance
        if_rebal = True if dates[t] in rebaldates else False
        # if_rebal = ~np.isempty(np.find(rebaldates == dates[t]))
        if if_rebal:    # We need to rebalance
            SigStale = Sig # std and corr
            if if_debug:
                print('Rebalancing')
            if param['PortConstr'] == 'equal':
                wNew = portValCurrent*(np.ones(nAssets)/nAssets)
            if param['PortConstr'] == 'equalvol':
                vols = np.sqrt(np.diagonal(Sig))
                volsinv = 1./vols
                volsinvsum = sum(volsinv)
                wNew = portValCurrent*(volsinv/volsinvsum)
            if param['PortConstr'] == 'mv':
                # Here lambda stands for 2*lambda!!!
                lambda2 = 8;
                # Long-short
                wNew = portValCurrent*np.quadprog(Sig*lambda2,-mu,[],[],np.ones(1,len(Sig)),1)
        else:
            # We don't need to rebalance
            wNew = wCurrent
        W[:,t] = wNew
        RiskProj[t] = np.sqrt(wNew*Sig*wNew)/sum(wNew)
        RiskContr[:,t] = wNew*(SigStale*wNew/(wNew*SigStale*wNew))
        # RiskContrProj(:,t) = wNew*(Sig*wNew/(wNew*Sig*wNew))
        trades = wNew - wCurrent
        turnover[t] = sum(abs(trades))/portValCurrent
        
        # Calculate portfolio at the end of the period
        # (If needed in the futute, add cash position here)
        wCurrent = wNew*(np.ones(len(Rets))+Rets[:,t])
        securityRet[:,t-1] = wNew*Rets[:,t]
        portValCurrent = sum(wCurrent)
        portVal[t] = portValCurrent
        if portVal[t] < 0:
            raise Exception('Port val less than zero!{}\n'.format(t))
        portRet[t-1] = (portVal[t]-portVal[t-1])/portVal[t-1]
        retdates[t-1] = dates[t]
    
    # Populate output structure
    output_struct = {}
    output_struct['portVal'] = portVal
    output_struct['dates'] = dates
    output_struct['W'] = W
    output_struct['RiskContrProj'] = RiskContr
    output_struct['RiskProj'] = RiskProj
    output_struct['cash'] = cash
    output_struct['turnover'] = turnover
    output_struct['secnames'] = secnames
    output_struct['securityRet'] = securityRet
    output_struct['portRet'] = portRet
    output_struct['retdates'] = retdates    
    
    return output_struct
