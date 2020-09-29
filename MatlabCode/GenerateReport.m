function [ output_args ] = GenerateReport(output_struct,filename,doctype)
% This function generates outputs and reports from a backtest created by
% BackTest.

% Petter Kolm Copyright 2012-2016. 
%
% This file cannot be redistributed without the explicit permission
% of Petter Kolm, Petter.Kolm@nyu.edu.
%
% Please report any bugs to Petter.Kolm@nyu.edu


freq = 260; % hardcoded for daily data for now (YOU NAY WANT TO CHANGE THIS)
%
dollarscale = 10^6; % scale dollar to millions of dollars

% Unpack the inputs
portVal = output_struct.portVal;
dates = output_struct.dates;
W = output_struct.W;
RiskContrProj = output_struct.RiskContrProj;
RiskProj = output_struct.RiskProj;
cash = output_struct.cash;
turnover = output_struct.turnover;
secnames = output_struct.secnames;
securityRet = output_struct.securityRet;
portRet = output_struct.portRet;
retdates = output_struct.retdates;

nAssets = length(secnames);

% Summary statistics
% . . . Since inception 
summary_incep = PortSummaryStats(output_struct,1, length(retdates), freq)

% . . . Last 5 years
summary_5 = PortSummaryStats(output_struct,length(retdates)-5*freq+1,length(retdates), freq)

% . . . Last 3 years
summary_3 = PortSummaryStats(output_struct,length(retdates)-3*freq+1,length(retdates), freq)

% . . . Last 1 year
summary_1 = PortSummaryStats(output_struct,length(retdates)-freq+1,length(retdates), freq)


% Produce outputs & generate report
% . . . Create a report
images = {}; %cell array to hold images for the report
import mlreportgen.dom.*;
report = Document(filename,doctype);
%
% YOU MAY WANT TO ADD ADDITIONAL ITEMS HERE TO PRINT TO THE FILE. FOR
% EXAMPLE, BACKTEST PARAMETERS AND OTHER SETTINGS
%
append(report, ['This report was generated on ', datestr(datetime('now')), ' by Shaolun Du.']);
append(report, ['Securities used:']);
for i=1:nAssets,
    append(report, secnames(i));
end

% . . . Summary stats
nfig = 1;
f = figure(nfig), 
set(f,'Position',[500 500 300 150]);

dat =  {'        Ann. Ret (%)', summary_incep.ann_ret,summary_5.ann_ret,summary_3.ann_ret,summary_1.ann_ret;...
        '        Ann. Vol (%)', summary_incep.ann_vol, summary_5.ann_vol,summary_3.ann_vol,summary_1.ann_vol;...   
        '        Sharpe', summary_incep.ann_Sharpe, summary_5.ann_Sharpe,summary_3.ann_Sharpe,summary_1.ann_Sharpe;...
        '        Skew',  summary_incep.skew, summary_5.skew,summary_3.skew,summary_1.skew;...
        '        Kurtosis', summary_incep.kurtosis,summary_5.kurtosis,summary_3.kurtosis,summary_1.kurtosis;...
        '        Drawdown (%)', summary_incep.drawdown,summary_5.drawdown,summary_3.drawdown,summary_1.drawdown;};
columnname =   {'________________','Inception', '5 years', '3 years', '1 year'};
columnformat = {'char', 'numeric', 'numeric', 'numeric','numeric'};
t = uitable('Units','normalized',... 
    'Position',[0.05 0.05 0.755 0.87],...   %'Position',[50 50 70 80],...
    'Data', dat,...
    'ColumnName', columnname,...
    'ColumnFormat', columnformat,...
    'RowName',[]);
t.Position(3) = t.Extent(3);      
t.Position(4) = t.Extent(4);     
img = AddPlot(report, 'Stats');
images = [images {img}];
        
% . . . Portfolio value & return
nfig = nfig + 1; 
figure(nfig), [ax,hLine1,hLine2] = plotyy(retdates,portRet*100,dates,portVal/dollarscale,'plot','plot');
title('Portfolio Return (lhs) and Portfolio Value (rhs)');
xlabel('Time');
ylabel(ax(1),'Return (%)');
ylabel(ax(2),'Dollars (Millions)');
ax(1).YColor = [0 0 1]; % dark blue
ax(2).YColor = [1 0 0]; % red
hLine1.LineWidth = 2;
hLine1.Color = [0 0 1]; %red 
hLine2.LineWidth = 2;
hLine2.Color = [1 0 0]; %red 
datetick(ax(1),'keeplimits');
datetick(ax(2),'keeplimits');
legend('Return','Value','Location','Best');
img = AddPlot(report, 'plotRet');
images = [images {img}];

% . . . Portfolio return & vol
lookback = 22;
portVar = zeros(length(portRet),1);
for t=1:length(portRet),
    if t<lookback
        [tmp1, portVar(t), tmp2] = ewstats(portRet(1:t), 1, t);
    else
        [tmp1, portVar(t), tmp2] = ewstats(portRet(1:t), 1, lookback);
    end
end
nfig = nfig + 1;
figure(nfig), [ax,hLine1,hLine2] = plotyy(retdates,portRet*100,retdates,sqrt(portVar)*100,'plot','plot');
title(['Daily Portfolio Return (lhs) and Volatility (rhs) (lookback = ' num2str(lookback) ')']);
xlabel('Time');
ylabel(ax(1),'Return (%)');
ylabel(ax(2),'Volatility (%)');
ax(1).YColor = [0 0 1]; % dark blue
ax(2).YColor = [1 0 0]; % red
hLine1.LineWidth = 2;
hLine1.Color = [0 0 1];
hLine2.LineWidth = 2;
hLine2.Color = [1 0 0];
datetick(ax(1),'keeplimits');
datetick(ax(2),'keeplimits');
legend('Return','Volatilty','Location','Best');
img = AddPlot(report, 'plotVol');
images = [images {img}];

% . . . Portfolio Sharpe
lookback = 6*22;
portAvgRet = zeros(length(portRet),1);
portVar = zeros(length(portRet),1);
portSharpe = zeros(length(portRet),1);
for t=1:length(portRet),
    if t<lookback
        [portAvgRet(t), portVar(t), tmp2] = ewstats(portRet(1:t), 1, t);
        % When the available history isn't long enough (i.e. < lookback)
        % estimates are not as reliable. We'll cap them in [-0.5,0.5]
        portSharpe(t) = portAvgRet(t)/sqrt(portVar(t));
        portSharpe(t) = min(max(portSharpe(t),-0.5),0.5);
    else
        [portAvgRet(t), portVar(t), tmp2] = ewstats(portRet(1:t), 1, lookback);
        portSharpe(t) = portAvgRet(t)/sqrt(portVar(t));
    end
end
nfig = nfig + 1;
figure(nfig), [hLine] = plot(retdates,portSharpe);
figure(nfig), [ax,hLine1,hLine2] = plotyy(retdates,portSharpe*sqrt(260),retdates,sqrt(portVar)*100*sqrt(260),'plot','plot');
title(['Annualized Portfolio Sharpe Ratio (lhs) and Volatility (rhs) (lookback = ' num2str(lookback) ')']);
xlabel('Time');
ylabel(ax(1),'Sharpe');
ylabel(ax(2),'Volatility (%)');
ax(1).YColor = [0 0 1]; % dark blue
ax(2).YColor = [1 0 0]; % red
hLine1.LineWidth = 2;
hLine1.Color = [0 0 1];
hLine2.LineWidth = 2;
hLine2.Color = [1 0 0];
datetick(ax(1),'keeplimits');
datetick(ax(2),'keeplimits');
legend('Sharpe','Volatilty','Location','Best');
img = AddPlot(report, 'plotSharpe');
images = [images {img}];

% . . . Portfolio projected risk & realized risk
lookback = 3*22;
portVar = zeros(length(portRet),1);
for t=1:length(portRet),
    if t<lookback
        [tmp1, portVar(t), tmp2] = ewstats(portRet(1:t), 1, t);
    else
        [tmp1, portVar(t), tmp2] = ewstats(portRet(1:t), 1, lookback);
    end
end
nfig = nfig + 1;
figure(nfig), [ax,hLine1,hLine2] = plotyy(retdates,RiskProj(1:end-1)*100,retdates,sqrt(portVar)*100,'plot','plot');
title(['Daily Projected Portfolio Risk (lhs) and Volatility (rhs) (lookback = ' num2str(lookback) ')']);
xlabel('Time');
ylabel(ax(1),'Projected Volatility (%)');
ylabel(ax(2),'Volatility (%)');
ax(1).YColor = [0 0 1]; % dark blue
ax(2).YColor = [1 0 0]; % red
hLine1.LineWidth = 2;
hLine1.Color = [0 0 1];
hLine2.LineWidth = 2;
hLine2.Color = [1 0 0];
ax(2).YLim = ax(1).YLim;
datetick(ax(1),'keeplimits');
datetick(ax(2),'keeplimits');
legend('Projected Volatility','Volatilty','Location','Best');
img = AddPlot(report, 'plotRiskProj');
images = [images {img}];
% . . . . . . Scatter plot
nfig = nfig + 1;
figure(nfig), [hLine1] = scatter(RiskProj(1:end-1)*100,sqrt(portVar)*100);
title(['Daily Projected Volatility (x) and Volatility (y) (lookback = ' num2str(lookback) ')']);
xlabel('Projected Volatility (%)');
ylabel('Volatility (%)');
hLine1.LineWidth = 2;
hLine1.MarkerEdgeColor = [0 0 1];
axis equal; 
ax = gca;
maxPoint = max([ax.XLim ax.YLim])
ax.XLim = [0 maxPoint];
ax.YLim = [0 maxPoint];
hold on;
hLine2 = plot([0 maxPoint],[0 maxPoint]);
hLine2.Color = [1 0 0];
hLine2.LineWidth = 2;
hold off;
img = AddPlot(report, 'plotRiskProjVolScatter');
images = [images {img}];

% . . . Max Drawdown
lookback = 260;
portMaxDrawdown = zeros(length(portRet),1);
MaxDrawdownIdx = zeros(2,length(portRet));
for t=1:length(portRet),
     if t<lookback
         [portMaxDrawdown(t), MaxDrawdownIdx(:,t)] = maxdrawdown(ret2tick(portRet(1:t)),'return');
     else
         [portMaxDrawdown(t), MaxDrawdownIdx(:,t)] = maxdrawdown(ret2tick(portRet(t-lookback+1:t)),'return');
     end
end
startIdx = [1 MaxDrawdownIdx(1,2:end)-1]; % need to subtract with one to adjust for the fact the the cum series has one more element
endIdx =  [1 MaxDrawdownIdx(2,2:end)-1];
nfig = nfig + 1;
figure(nfig), [ax,hLine1,hLine2] = plotyy(retdates,-portMaxDrawdown*100,dates,portVal/dollarscale,'plot','plot');
title(['Portfolio Drawdown (lhs)(lookback = ' num2str(lookback) ') and Portfolio Value (rhs)']);
xlabel('Time');
ylabel(ax(1),'Drawdown (%)');
ylabel(ax(2),'Dollars (Millions)');
ax(1).YColor = [0 0 1]; % dark blue
ax(2).YColor = [1 0 0]; % red
hLine1.LineWidth = 2;
hLine1.Color = [0 0 1];
hLine2.LineWidth = 2;
hLine2.Color = [1 0 0];
datetick(ax(1),'keeplimits');
datetick(ax(2),'keeplimits');
legend('Drawdown','Value','Location','Best');
img = AddPlot(report, 'plotMaxDarawdown');
images = [images {img}];

% . . . Turnover
nfig = nfig + 1;
figure(nfig), [hLine] = plot(dates,turnover*100);
title('Portfolio Turnover')
xlabel('Time')
ylabel('Turnover (%)')
hLine.LineWidth = 2;
hLine.Color = [0 0 1];
ax = gca;
datetick(ax,'keeplimits');
img = AddPlot(report, 'plotTurnover');
images = [images {img}];

% . . . Portfolio weights (in dollars)
% . . . (Not plotting cash as we assume that we are always fully invested)
nfig = nfig + 1;
figure(nfig), hArea = area(dates, W'/dollarscale);
title('Portfolio Weights');
xlabel('Time');
ylabel('Dollars (Millions)');
ax = gca;
datetick(ax,'keeplimits');
hLegend = legend(secnames,'Interpreter','none','Location','northoutside');
img = AddPlot(report, 'plotWeightsDollars');
images = [images {img}];

% . . . Portfolio weights (in percent)
% . . . (Not plotting cash as we assume that we are always fully invested)
nfig = nfig + 1;
Wsum = repmat(sum(W,1)+cash',nAssets,1);
Wperc = W./ Wsum;
figure(nfig), area(dates, Wperc');
title('Portfolio Weights')
xlabel('Time')
ylabel('Weights (%)')
ax = gca;
datetick(ax,'keeplimits');
ax.YLim(2) = 1;  % In a long-only portfolio, weights add up to 100%
hLegend = legend(secnames,'Interpreter','none','Location','northoutside');
img = AddPlot(report, 'plotWeightsPercent');
images = [images {img}];

% . . . Projected Risk contribution
nfig = nfig + 1;
figure(nfig), area(dates, RiskContrProj');
title('Projected Risk Contributions')
xlabel('Time')
ylabel('Risk Contribution (%)')
ax = gca;
datetick(ax,'keeplimits');
ax.YLim(2) = 1;  % In a long-only portfolio, weights add up to 100%
hLegend = legend(secnames,'Interpreter','none','Location','northoutside');
img = AddPlot(report, 'plotRiskContrProj');
images = [images {img}];

% . . . Realized Risk contribution
lookback = 6*22;
RiskContr = zeros(nAssets,length(portRet));
securityCov = zeros(nAssets,nAssets,length(portRet));
iota = ones(nAssets,1);
%EE = eye(nAssets);
for t=1:length(portRet),
    if t<lookback
        [tmp1, securityCov(:,:,t), tmp2] = ewstats(securityRet(:,1:t)', 1, t);
    else
        [tmp1, securityCov(:,:,t), tmp2] = ewstats(securityRet(:,1:t)', 1, lookback);
    end
        RiskContr(:,t) = iota .* (securityCov(:,:,t)*iota /(iota'*securityCov(:,:,t)*iota)); 
end
nfig = nfig + 1;
figure(nfig), area(retdates, RiskContr');
title(['Realized Risk Contributions (lookback = ' num2str(lookback) ')']);
xlabel('Time')
ylabel('Risk Contribution (%)')
ax = gca;
datetick(ax,'keeplimits');
ax.YLim = [0 1];  % In a long-only portfolio, weights add up to 100%
hLegend = legend(secnames,'Interpreter','none','Location','northoutside');
img = AddPlot(report, 'plotRiskContr');
images = [images {img}];

close(report);

% Delete images
for i = 1:length(images)
    delete(images{i});
end

%rptview(report.OutputPath,'pdf');

end

