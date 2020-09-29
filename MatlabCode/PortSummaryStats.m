function [summary_stats] = PortSummaryStats(output_struct,start_idx, end_idx, freq)
% This function produces portfolio summary statistics

portRet = output_struct.portRet;
retdates = output_struct.retdates;

% Index and dates
summary_stats.start_idx = start_idx;
summary_stats.end_idx = end_idx;
summary_stats.startdate = retdates(start_idx); 
summary_stats.enddate = retdates(end_idx);

portRet = portRet(start_idx:end_idx);

% Annualized return, vol, and Sharpe
summary_stats.ann_ret = mean(portRet)*freq*100;
summary_stats.ann_vol = std(portRet)*sqrt(freq)*100;
summary_stats.ann_Sharpe = mean(portRet)/std(portRet)*sqrt(freq);

% Skew and kurtosis
summary_stats.skew = skewness(portRet);
summary_stats.kurtosis = kurtosis(portRet);

% Max drawdown
[drawdown, tmp] = maxdrawdown(ret2tick(portRet),'return');
summary_stats.drawdown = -drawdown*100; 
return