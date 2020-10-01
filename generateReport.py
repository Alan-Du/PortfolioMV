# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:31:08 2020
This function generates outputs and reports 
from a backtest created by BackTest.py.

@author: Shaolun du
@contact: shaolun.du@gmail.com
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from maxDrawDown import maxDrawDown as maxDrawDown
from scipy.stats import gmean

def generateReport(output_struct):
    outDir      = "outPuts\\" # output directory name
    freq        = 260  # hardcoded for daily data for now
    dollarscale = output_struct['portVal'][0] # scale dollar to millions of dollars
    
    # Unpack the inputs
    portVal       = output_struct['portVal']
    dates         = output_struct['dates']
    W             = output_struct['W']
    RiskContrProj = output_struct['RiskContrProj']
    RiskProj      = output_struct['RiskProj']
    cash          = output_struct['cash']
    turnover      = output_struct['turnover']
    secnames      = output_struct['secnames']
    securityRet   = output_struct['securityRet']
    portRet       = output_struct['portRet']
    retdates      = output_struct['retdates']
    nAssets       = len(secnames)
    summary       = output_struct['smy']
    strat         = output_struct['PortConstr']
    
    # Start plot report
    fig = plt.figure(figsize=(18,38))
    fig.suptitle(strat+' portfolio BackTest Output', fontsize=35)
    gs = fig.add_gridspec(4,2)
    """  Plot one summary table of strategy
    """
    ax0 = fig.add_subplot(gs[0, :])
    ax0.axis('off')
    rcolors = plt.cm.BuPu(np.full(len(summary.index), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(summary.columns), 0.1))
    ytb = ax0.table(cellText=summary.values,
                    colWidths = [0.15]*len(summary.columns),
                    rowColours=rcolors,
                    colColours=ccolors,
                    rowLabels=summary.index,
                    colLabels=summary.columns,
                    cellLoc = 'center', rowLoc = 'center',
                    loc='center')
    ytb.set_fontsize(20)
    ytb.scale(1, 6)
    """  Plot two portVal vs rets and volatility
    """
    ax1 = fig.add_subplot(gs[1,0])
    ax1.plot(dates, portVal, color="navy")
    ax1.set_xlabel("Dates",fontsize=14)
    ax1.set_ylabel("PortVal",color="navy",fontsize=14)
    ax1.set_title('PortVal vs Rets')
    axx=ax1.twinx()
    axx.bar(dates, portRet, color="green",width=1.5)
    axx.set_ylabel("Return",color="green",fontsize=14)
    
    # plot portval vs vol
    # compute portfolio volatility
    lookback = 22 # volatility lookback
    portVol = []
    for i in range(len(dates)):
        if i < lookback:
            portVol.append(np.std(portRet[:i]))
        else:
            portVol.append(np.std(portRet[i-lookback:i]))
    ax2 = fig.add_subplot(gs[1,1])
    ax2.plot(dates, portVal, color="navy")
    ax2.set_xlabel("Dates",fontsize=14)
    ax2.set_ylabel("PortVal",color="navy",fontsize=14)
    ax2.set_title('PortVal vs 1M-Vol')
    axx=ax2.twinx()
    axx.bar(dates, portVol, color="tomato",width=1.5,alpha=0.5)
    axx.set_ylabel("1M-Vol",color="tomato",fontsize=14)
    
    """  Plot three portSharpe, MDD, weights, turnover
    """
    lookback = 22*6 # sharpe lookback
    portShp,portVol = [],[]
    for i in range(len(dates)):
        if i < lookback:
            vol  = np.std(portRet[:i])
            rets = gmean(portRet[:i]+1)-1
        else:
            vol  = np.std(portRet[i-lookback:i])
            rets = gmean(portRet[i-lookback:i]+1)-1
        portVol.append(vol)
        portShp.append(rets/vol)
    # plot portval vs returns
    ax3 = fig.add_subplot(gs[2,0])
    ax3.plot(dates, portVal, color="navy")
    ax3.set_xlabel("Dates",fontsize=14)
    ax3.set_ylabel("portSharpe",color="navy",fontsize=14)
    ax3.set_title('6M-Sharpe vs 6M-Vol')
    axx=ax3.twinx()
    axx.bar(dates, portVol, color="tomato",width=1.5,alpha=0.5)
    axx.set_ylabel("6M-Vol",color="tomato",fontsize=14)
    
    # compute portfolio MDD
    lookback = freq # ann lookback
    portMDD = []
    for i in range(len(dates)):
        if i < lookback:
            portMDD.append(maxDrawDown(portVal[:i]))
        else:
            portMDD.append(maxDrawDown(portVal[i-lookback:i]))
    ax4 = fig.add_subplot(gs[2,1])
    ax4.plot(dates, portVal, color="navy")
    ax4.set_xlabel("Dates",fontsize=14)
    ax4.set_ylabel("portVal",color="navy",fontsize=14)
    ax4.set_title('portVal vs 12M-MDD')
    axx=ax4.twinx()
    axx.fill_between(dates, portMDD, color="darkgray",alpha=0.5)
    axx.set_ylabel("annMaxDrawDown",color="darkgray",fontsize=14)
    
    # portfolio turnover ratio
    ax5 = fig.add_subplot(gs[3,0])
    ax5.fill_between(dates, turnover, color="navy", alpha=0.5)
    ax5.set_xlabel("Dates",fontsize=14)
    ax5.set_ylabel("portTurnover",color="navy",fontsize=14)
    ax5.set_title('portTurnover')
    # portfolio weights ratio
    temp = []
    for t in range(len(dates)):
        temp.append(W[:,t])
    weights = list(zip(*temp))
    ax6 = fig.add_subplot(gs[3,1])
    ax6.stackplot(dates, weights, labels=secnames)
    ax6.set_xlabel("Dates",fontsize=14)
    ax6.set_ylabel("portWeights",color="navy",fontsize=14)
    ax6.legend(loc='upper left')
    ax6.set_title('portWeights')
    #plt.tight_layout()
    fig.savefig(outDir+strat+'BackTestDetails.png')
    return None
