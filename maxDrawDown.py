# -*- coding: utf-8 -*-
"""
This funtion calcualte maxdrawdown 
based on return series 
@author: Shaolun Du
@contact: Shaolun.du@gmail.com
"""
def maxDrawDown(vals):
    # rets is portfolio returns
    # on daily basis
    # return = maxDrawDown
    mDD, cur_max = 0,0
    for level in vals:
        cur_max = max(cur_max,level)
        mDD = max((cur_max-level)/cur_max,mDD)
    return -mDD