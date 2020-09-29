function output_struct = Backtest(param,Data,if_debug)
% This function perform a backtest of portfolio of risky securities.
% The portfolio can be constructed in several different ways:
% (1) Equal weighting (equal),
% (2) Equal vol-weighting (equalvol),
% (3) Global minimum variance portfolio, and  (FOR YOU TO IMPLEMENT)
% (4) Mean-Variance optimization (mv)         (FOR YOU TO IMPLEMENT)
% 
% Inputs: 
%     param - structure that specifies the backtest to run
%     Data  - dataset (factor returns and covariances, security names, and
%             rebalancing dates)
%
% Outputs:
%     output_struct - structure with extensive outputs
%
% Notes:
% 1. We assume the first portfolio is all in cash
% 2. Portfolio weights are stored in their cash allocation (dollars) and indexed such that W(t) align with Rets(t):
% (a) Rets(t) corresponds to the security return over the time period (t-1,t]
% (b) W(t) corresponds to the portfolio weights held over the time period (t-1,t]
% 3. The value of the portfolio is calculated at the end of each time
% period. In other words, if the time period is (t-1,t] the portfolio value
% is calculated at time t.

% Petter Kolm Copyright 2012-2016. 
%
% This file cannot be redistributed without the explicit permission
% of Petter Kolm, Petter.Kolm@nyu.edu.
%
% Please report any bugs to Petter.Kolm@nyu.edu


secnames = Data.secnames;
Rets = Data.Rets;
dates = Data.dates; 
COV = Data.COV;
ER = Data.ER;
rebaldates = Data.rebaldates;
nAssets = Data.param_Data.nAssets;

% Define variables anbd allocate space
T = length(dates);
cash = zeros(T,1);
tcosts = zeros(T,1);
turnover = zeros(T,1);
portVal = zeros(T,1);
portRet = zeros(T-1,1);
retdates = zeros(T-1,1);
W = zeros(nAssets,T);
RiskContr = zeros(nAssets,T-1);
securityRet = zeros(nAssets,T-1);
RiskProj = zeros(T-1,1);

% At t = 1
% . . . Initial portfolio value (i.e. value at starttime) and risk factor
% allocations
cash(1) = param.capital;
portVal(1) = cash(1);

portValCurrent = portVal(1);
wCurrent = W(:,1);
% Now move forward in time and rebalalance when needed
for t = 2:T,
    if if_debug
        t
    end
    % Covariance matrix 
    Sig = COV(:,:,t);
    mu = ER(:,t);
    % Determine if we need to rebalance
    if_rebal = ~isempty(find(Data.rebaldates == dates(t)));
    if if_rebal    %% We need to rebalance
        SigStale = Sig;
        if if_debug
            disp('Rebalancing');
        end
        switch param.PortConstr
            case {'equal'}
                wNew = portValCurrent .* (ones(nAssets,1)/nAssets);
            case {'equalvol'}
                vols = sqrt(diag(Sig));
                volsinv = 1./vols;
                volsinvsum = sum(volsinv);
                wNew = portValCurrent .* (volsinv/volsinvsum);
            case {'gmv'}
                % FOR YOU TO IMPLEMENT USING QUADPROG
                % Long-short
%                 wNew = portValCurrent.*quadprog(Sig,[],[],[],ones(1,size(Sig,1)),1);
%                 % Long-only
                 wNew = portValCurrent.*quadprog(Sig,[],[],[],ones(1,size(Sig,1)),1,zeros(size(Sig,1),1));
            case {'mv'}
                % FOR YOU TO IMPLEMENT USING QUADPROG
                % Here lambda stands for 2*lambda!!!
                lambda2 = 8;
                % Long-short
%                 wNew = portValCurrent.*quadprog(Sig*lambda2,-mu',[],[],ones(1,size(Sig,1)),1);
%                 % Long-only
                wNew = portValCurrent.*quadprog(lambda2*Sig,-mu',[],[],ones(1,size(Sig,1)),1,zeros(size(Sig,1),1));
        end
    else %% We don't need to rebalance
        wNew = wCurrent;
    end
    W(:,t) = wNew;
    RiskProj(t) = sqrt(wNew'*Sig*wNew)/sum(wNew);
    RiskContrProj(:,t) = wNew.*(SigStale*wNew/(wNew'*SigStale*wNew));
    %RiskContrProj(:,t) = wNew.*(Sig*wNew/(wNew'*Sig*wNew));
    trades = wNew - wCurrent;
    turnover(t) = sum(abs(trades))/portValCurrent;
    
    % Calculate portfolio at the end of the period
    % (If needed in the futute, add cash position here)
    wCurrent = wNew .* (ones(size(Rets,1),1)+Rets(:,t));
    securityRet(:,t-1) = wNew .* Rets(:,t);
    portValCurrent = sum(wCurrent);
    portVal(t) = portValCurrent;
     if portVal(t) < 0
         fprintf('Here val less than zero! %d\n',t);
         portVal(t)
         portVal(t-1)
         portVal(t-2)
         portVal(t-3)
         error('1');
     end
     portRet(t-1) = (portVal(t)-portVal(t-1))./portVal(t-1);
    retdates(t-1) = dates(t);
end

% Populate output structure
output_struct.portVal = portVal;
output_struct.dates = dates;
output_struct.W = W;
output_struct.RiskContrProj = RiskContrProj;
output_struct.RiskProj = RiskProj;
output_struct.cash = cash;
output_struct.turnover = turnover;
output_struct.secnames = Data.secnames;
output_struct.securityRet = securityRet;
output_struct.portRet = portRet;
output_struct.retdates = retdates;

return

