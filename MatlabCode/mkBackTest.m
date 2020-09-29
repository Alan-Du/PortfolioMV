% This script that calls the BackTest function to perform backtests of
% portfolios of securities.

% Petter Kolm Copyright 2012-2016. 
%
% This file cannot be redistributed without the explicit permission
% of Petter Kolm, Petter.Kolm@nyu.edu.
%
% Please report any bugs to Petter.Kolm@nyu.edu


% Clear working space and all figures
clear all;
close all;

% Start clock
tic

% Degugging?
if_debug = 0; % turn off debugging output
%if_debug = 1; % turn on degugging output

% Data
% param.datasource = 'TestData';  % test data
param.datasource = 'HW3_3_1';  % real data
load([param.datasource '.mat']);

% All data is daily; assuming 260 days in a year
param.freq = 260;

% Number of assets
nAssets = length(Data.secnames);

% General backtest parameters
param.capital = 100*10^6; % initial cash position in dollars
param.output_filename = [param.datasource '_output']; % *.mat file where numerical outputs are stored
%param.PortConstr = 'equal'; % equal weights
%param.PortConstr = 'equalvol'; % equal volatility in all assets
%param.PortConstr = 'gmv'; % gmv
 param.PortConstr = 'mv'; % mv
param.outputdoc = [param.PortConstr '_output'];

% Parameters for the reports
doctype = 'docx';

res_incep = [];
res_fiveYrs = [];
res_threeYrs = [];
res_oneYr = [];

% Run backtest
outputBackTest = BackTest(param,Data,if_debug);
GenerateReport(outputBackTest,param.outputdoc,doctype);

[res_incep, res_fiveYrs, res_threeYrs, res_oneYr,...
    columnname_incep, columnname_fiveYrs, columnname_threeYrs, columnname_oneYr] =...
    PortSummaryStatsAll(outputBackTest,param);

% Stop clock
toc
