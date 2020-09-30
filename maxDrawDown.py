# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:54:51 2020
This funtion calcualte maxdrawdown 
based on return series 
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
def maxDrawDown(rets):
    # rets is portfolio returns
    # on daily basis
    # return = maxDrawDown
    mDD = 0
    level,cur_max = 1,0
    for ele in rets:
        level *= (ele+1)
        cur_max = max(cur_max,level)
        mDD = max(cur_max-level,mDD)
    return -mDD