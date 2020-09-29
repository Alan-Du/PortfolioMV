function [res_incep, res_fiveYrs, res_threeYrs, res_oneYr, columnname_incep, columnname_fiveYrs, columnname_threeYrs, columnname_oneYr] = PortSummaryStatsAll(output_struct,param)

nDays = length(output_struct.retdates);
freq = param.freq;
PortConstr = param.PortConstr;

% Since inception
summary = PortSummaryStats(output_struct,1,             nDays, freq);
incep = [summary.ann_ret; summary.ann_vol; summary.ann_Sharpe; summary.skew; summary.kurtosis; summary.drawdown];
% Last 5 years
summary = PortSummaryStats(output_struct,nDays-5*freq+1,nDays, freq);
fiveYrs = [summary.ann_ret; summary.ann_vol; summary.ann_Sharpe; summary.skew; summary.kurtosis; summary.drawdown];
% Last 3 years
summary = PortSummaryStats(output_struct,nDays-3*freq+1,nDays, freq);
threeYrs = [summary.ann_ret; summary.ann_vol; summary.ann_Sharpe; summary.skew; summary.kurtosis; summary.drawdown];
% Last 1 year
summary = PortSummaryStats(output_struct,nDays-  freq+1,nDays, freq);
oneYr = [summary.ann_ret; summary.ann_vol; summary.ann_Sharpe; summary.skew; summary.kurtosis; summary.drawdown];

res_incep = incep';
res_fiveYrs = fiveYrs';
res_threeYrs = threeYrs';
res_oneYr = oneYr';

suffix = [PortConstr '_incep'];
columnname_incep = {['Ret_' suffix],['Vol_' suffix],['Sharpe_' suffix],['Skew_' suffix],...
    ['Kurtosis_' suffix],['Drawdown_' suffix]};
suffix = [PortConstr '_5yrs'];
columnname_fiveYrs = {['Ret_' suffix],['Vol_' suffix],['Sharpe_' suffix],['Skew_' suffix],...
    ['Kurtosis_' suffix],['Drawdown_' suffix]};
suffix = [PortConstr '_3yrs'];
columnname_threeYrs = {['Ret_' suffix],['Vol_' suffix],['Sharpe_' suffix],['Skew_' suffix],...
    ['Kurtosis_' suffix],['Drawdown_' suffix]};
suffix = [PortConstr '_1yr'];
columnname_oneYr = {['Ret_' suffix],['Vol_' suffix],['Sharpe_' suffix],['Skew_' suffix],...
    ['Kurtosis_' suffix],['Drawdown_' suffix]};

return
