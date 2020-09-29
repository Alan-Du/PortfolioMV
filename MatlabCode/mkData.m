% This script prepares a data structure called Data that is used 
% as in input to the portfolio backtester mkBackTest.m

% You can easily add additional data sources to this script by modifying
% the code below. 

% Petter Kolm Copyright 2012-2016. 
%
% This file cannot be redistributed without the explicit permission
% of Petter Kolm, Petter.Kolm@nyu.edu.
%
% Please report any bugs to Petter.Kolm@nyu.edu

% Clear working space and all figures
clear all;
close all;
% if_debug = 0;
if_debug = 1; % uncomment to turn on degugging output

rebalfreq = 'monthly';
%rebalfreq = 'quarterly';

%if_data = 0; % use generated test data
if_data = 1; % use historical data for industry portfolios

switch if_data
    
    case{0}
        disp('Creating simulated data'); 
        % Set parameters
        param_Data.nAssets = 10;
        nyears = 10;
        param_Data.T = nyears*260; % nyears of similayed daily history
        param_Data.startwin = 260; % use first year for estimation
        param_Data.decay = 1; % decay to use for cov and ER estimation
        param_Data.lookback = 260; % lookback period in days for ER and COV estimtation  
        param_Data.shrinkage = 0.5; % shrinkage for shrunk ERs
        param_Data.output_filename = 'TestData'; % name of *.mat file where data is stored
        param_Data.freq = 260; % daily Data
        param_data.seed = 5489;
        % We similate return Data from the normal disribution
        s = RandStream.create('mt19937ar','seed', param_data.seed); % fix the random feed so we get same sequence every time
        RandStream.setGlobalStream(s);
        Rets_tmp = randn(param_Data.T, param_Data.nAssets);
        
        % Generate simulated dates
        edate = datenum('1/31/2015');
        sdate = edate-nyears*390;
        bdates = busdays(sdate,edate);
        dates = bdates(length(bdates)-param_Data.T-1:end);
        
        % Generate security names
        fac = 1:param_Data.nAssets;
        secnames = cellstr(num2str((fac)'))';
        
        % Normalize Data to chosen mean and covariance
        % . . . By modifying the code below the desired sharpes, volatilities, means, and correlations
        % . . . can be changed
        sharpes = linspace(0.5/sqrt(param_Data.freq),0.6/sqrt(param_Data.freq),param_Data.nAssets);
        vols = linspace(0.10/sqrt(param_Data.freq),0.15/sqrt(param_Data.freq),param_Data.nAssets);
        mus = sharpes.*vols;
        correls = 0.7*ones(param_Data.nAssets,param_Data.nAssets);
        correls = tril(correls,-1)+triu(correls,1)+eye(param_Data.nAssets,param_Data.nAssets);
        Sig = diag(vols)*correls*diag(vols);
        C = chol(Sig);
        
        SigRets = cov(Rets_tmp);
        CRets = chol(SigRets);
        Rets = (Rets_tmp-repmat(mean(Rets_tmp),param_Data.T,1))/CRets;
        Rets = (Rets*C)+repmat(mus,param_Data.T,1);
        if if_debug
            % These should be (close to) zero 
            mus - mean(Rets)
            Sig - cov(Rets)
        end
        
        param_Data.mus = mus; % save ER used to generate simluated data
        param_Data.Sig = Sig; % save COV used to generate simluated data
        
    case{1}
        % FOR YOU TO IMPLEMENT TO ADD INDUSTRY FACTORS ETC
        load 30IndPort_Clean.mat
        
        secnames = IndPort30_Clean.industry;
        param_Data.output_filename = 'HW3_3_1'; % name of *.mat file where data is stored
        param_Data.nAssets = 30;
        param_Data.T = length(IndPort30_Clean.date);
        param_Data.startwin = 260; % use first year for estimation
        param_Data.decay = 1; % decay to use for cov and ER estimation
        param_Data.lookback = 260; % lookback period in days for ER and COV estimtation  
        param_Data.shrinkage = 0.5; % shrinkage for shrunk ERs
        %   pay attention to dates
        dates = zeros(1,length(IndPort30_Clean.date));
        for i = 1:length(IndPort30_Clean.date)
            dates(i) = datenum(num2str(IndPort30_Clean.date(i)),'yyyymmdd');
        end
        % Daily basis in % scale
        Rets = IndPort30_Clean.Return/100;
        Sig = cov(IndPort30_Clean.Return);
        param_Data.mus = mean(Rets); % save ER used to generate simluated data
        param_Data.Sig = Sig; % save COV used to generate simluated data
   
    otherwise
        disp('Unknown value of if_testdata')
        if_testdata
        stop
end

% Estimate covariance matrices
time = zeros(param_Data.T-param_Data.startwin+1, 1);
ER = zeros(param_Data.nAssets,param_Data.T-param_Data.startwin+1);
shrunkER = zeros(param_Data.nAssets,param_Data.T-param_Data.startwin+1);
COV = zeros(param_Data.nAssets,param_Data.nAssets,param_Data.T-param_Data.startwin+1);
 
for t=param_Data.startwin:param_Data.T,
    i = t-param_Data.startwin+1;
    [ER(:,i), COV(:,:,i)] = ewstats(Rets(1:t,:),param_Data.decay,param_Data.lookback);
    shrunkER(:,i)=(1-param_Data.shrinkage)*ER(:,i)+param_Data.shrinkage*(mean(ER(:,i)));
end

% Populate data structure
Data.secnames = secnames; 
Data.Rets = Rets(param_Data.startwin:param_Data.T,:)'; % transpose Rets so they are aligned with ERs anc covs
Data.dates = dates(param_Data.startwin:param_Data.T);
Data.COV = COV;
Data.ER = ER; 
Data.shrunkER = shrunkER;

% . . . Define last business day of the month as rebalancing date
disp(['Rebalancing is set to ' rebalfreq]);
Data.rebaldates = busdays(Data.dates(2),Data.dates(end),rebalfreq);
% . . . . . . Make 2nd date in dates a trading day, if it is not already
% . . . . . . present amongst the rebalance dates
if Data.rebaldates(1) ~= Data.dates(2)
    Data.rebaldates = [Data.dates(2); Data.rebaldates];
end
% . . . . . . Make sure these rebalancing dates are present in the dates
% . . . . . . vector. If not, then remove the rebalancing dates that are not.
ind = [];
for i=1:length(Data.rebaldates)
    if ~isempty(find(Data.dates == Data.rebaldates(i)))
        ind = [ind i];
    else
        disp(['Creating rebalancing dates: Removing index ' num2str(i)]);
    end
end
Data.rebaldates(ind);
Data.rebalfreq = rebalfreq;

% . . . Save parameters used to estimate COVs
Data.param_Data = param_Data; 
    
% Save all output to file  
save(param_Data.output_filename,'Data');  

if if_debug
    plotmatrix(Data.Rets')
    mean(Data.Rets')*260
    std(Data.Rets')*sqrt(260)
    (mean(Data.Rets') ./ std(Data.Rets'))*sqrt(260)
    skewness(Data.Rets')
    kurtosis(Data.Rets')
    max(Data.Rets')
    min(Data.Rets')
end

