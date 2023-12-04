treenum = 50000;


set(0, 'defaultUicontrolFontName', 'Times New Roman');
set(0, 'defaultUitableFontName', 'Times New Roman');
set(0, 'defaultAxesFontName', 'Times New Roman');
set(0, 'defaultTextFontName', 'Times New Roman');
set(0, 'defaultUipanelFontName', 'Times New Roman');
% or any of the following...


%% Laod TreeData
    treeData = treeLoad(treenum);
    nodes = nodeTranslator(treeData);

%% Plot TreeData
     if ~isempty(nodes)
       plotTree(nodes{1}); 
     end

 


%% Export GoalNode to TreeNode xlsx
    nodeNearGoal = findNearGoalNode(nodes);
    nodeNearGoal = {nodeNearGoal};      
    
    
    nodeNearGoal = nodeNearGoal{1};

    pathNodes = getPathNodeAndSave(nodes{1}, nodeNearGoal,treenum);

    
    %%
    TotalDistance = plotPath(pathNodes);
    xMax = 1000;
    yMin = 530;

    xMin = 865;
    yMax = 560;
    rectangle('Position', [xMin, yMin, xMax-xMin, yMax-yMin], 'EdgeColor', 'r', 'FaceColor', 'r', 'LineWidth', 2);
    %% after this, run PythonCode!!!!!!!!!
    %% make Array(x,y,power,cost)
    fileName = "/home/esl/kyuyong/RRTstar/Power/Full" + num2str(treenum) + ".xlsx";
    pathData = table2array(readtable(fileName));
    FirstPowerArrayForPowerFigure = zeros(length(pathNodes),2);
    for i = 1:length(pathNodes)
        
        FirstPowerArrayForPowerFigure(i,:) = [pathData(i,1) pathNodes{1,i}.cost];
    end

%% plot
T = [0 ; diff(FirstPowerArrayForPowerFigure(:,2)) ];
P = FirstPowerArrayForPowerFigure(:,1);
E = P .* T / 1000; % kWs 단위로 변환
accumulateE = zeros(length(E),1);
accumulateE(1,1) = 0;
for i = 2:length(E)
    accumulateE(i,1) = sum(E(1:i,1));
end





% 누적 시간 계산
cumulativeTime = cumsum(T);

% 피규어 크기 설정 및 축 틱 길이, 폰트 설정
figure('Position', [100, 100, 1000, 800]); % 위치와 크기 설정
ax = gca; % 현재 축 핸들
ax.TickLength = [0.02 0.025]; % 틱 길이 조정
set(ax, 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'FontSize', 20); % 폰트 설정
clim([0 150]);
colormap(jet(41));
h = colorbar;

%ylabel(h, 'Velocity (km/h)','FontName', 'Times New Roman','FontWeight', 'bold', 'FontSize', 20);
ylabel(h, 'Velocity (km/h)','FontName', 'Times New Roman', 'FontSize', 20);
% 전체 트렌드를 나타내는 plot
%plot(cumulativeTime, accumulateE, 'b', 'LineWidth', 2); % 파란색 선, 굵은 선
hold on; % 현재 그래프 유지

% 각 노드의 점을 나타내는 scatter
for i = 1:length(pathNodes) - 1
        currentNode = pathNodes{i};
        nextNode = pathNodes{i + 1};
        
        avgVelocity = (currentNode.velocity + nextNode.velocity) / 2;
        
        % 컬러맵 크기를 41로 지정합니다.
        cmapSize = 41;
        
        % 정규화된 인덱스를 계산합니다.
        normalizedIndex = round((avgVelocity - 1) / 40 * cmapSize) + 1;
        normalizedIndex = max(min(normalizedIndex, cmapSize), 1);
        
        % 컬러맵에서 색상을 가져옵니다.
        color = jet(cmapSize);
        color = color(normalizedIndex, :);
        
        line([cumulativeTime(i,1), cumulativeTime(i+1,1)],[accumulateE(i,1),accumulateE(i+1,1)], 'Color',color , 'LineWidth', 6);
end
%scatter(cumulativeTime, accumulateE, 20, 'r', 'MarkerFaceColor', 'r'); % 빨간색 점, 검은색 테두리, 작은 크기




% 축 레이블 추가
xlabel('Time (s)', 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'FontSize', 20); % X축 레이블
ylabel('Accumulated Energy (kWs)', 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'FontSize', 20); % Y축 레이블

% Y축 틱 값 조정
yticks(0:1000:7000); % 0부터 70까지 10 단위로 틱 설정
yticklabels(arrayfun(@(x) sprintf('%d', x), 0:1000:7000, 'UniformOutput', false)); % 레이블 형식 지정

finalTime = cumulativeTime(end);
finalEnergy = accumulateE(end);
annotationText = sprintf('Total Time: %.2f s\nAccumulated Energy: %.2f kWs', finalTime, finalEnergy);

% 텍스트 상자 추가
annotation('textbox', [0.15, 0.8, 0.1, 0.1], 'String', annotationText, ...
    'FontSize', 19, 'FontWeight', 'bold', 'EdgeColor', 'k', 'BackgroundColor', 'white', ...
    'FontName', 'Times New Roman');

hold off; % 그래프 유지 해제
    
%% make secondOne

%% Plot TreeData
     if ~isempty(nodes)
       plotTree(nodes{1}); 
     end
    
    xMax = 1000;
    yMin = 530;

    xMin = 865;
    yMax = 560;
    rectangle('Position', [xMin, yMin, xMax-xMin, yMax-yMin], 'EdgeColor', 'r', 'FaceColor', 'r', 'LineWidth', 2);
 
    %% make Array(x,y,power,cost)
    fileName = "/home/esl/kyuyong/RRTstar/Power/Cut" + num2str(treenum) + ".xlsx";
    secondPathData = table2array(readtable(fileName));

    secondPowerArrayForPowerFigure = zeros(length(pathNodes),2);
    for i = 1:length(pathNodes)
        
        secondPowerArrayForPowerFigure(i,:) = [secondPathData(i,1) secondPathData(i,4)];
    end


 sT = [0 ; diff(secondPowerArrayForPowerFigure(:,2)) ];
 sP = secondPowerArrayForPowerFigure(:,1);
 sE = sP .* sT / 1000; % kWs 단위로 변환
 sAccumulateE = zeros(length(E),1);
 sAccumulateE(1,1) = 0;
 for i = 2:length(E)
     sAccumulateE(i,1) = sum(sE(1:i,1));
 end
% 누적 시간 계산
sCumulativeTime = cumsum(sT);
%% plot TrackPathofSecond

for i = 1:length(pathNodes) - 1
        currentVelocity = secondPathData(i,2);
        nextVelocity = secondPathData(i+1,2);
        
        avgVelocity = (currentVelocity + nextVelocity) / 2;
        
        % 컬러맵 크기를 41로 지정합니다.
        cmapSize = 41;
        
        % 정규화된 인덱스를 계산합니다.
        normalizedIndex = round((avgVelocity - 1) / 40 * cmapSize) + 1;
        normalizedIndex = max(min(normalizedIndex, cmapSize), 1);
        
        % 컬러맵에서 색상을 가져옵니다.
        color = jet(cmapSize);
        color = color(normalizedIndex, :);
        
        line([pathNodes{1,i}.x, pathNodes{1,i+1}.x],[pathNodes{1,i}.y, pathNodes{1,i+1}.y], 'Color',color , 'LineWidth', 6);
end
    annotationText = sprintf('Total Distance: %.2f (m)', TotalDistance);

    % 텍스트 상자 추가
    annotation('textbox', [0.2, 0.8, 0.1, 0.1], 'String', annotationText, ...
    'FontSize', 19, 'FontWeight', 'bold', 'EdgeColor', 'k', 'BackgroundColor', 'white', ...
    'FontName', 'Times New Roman');
    
    hold off; % 그래프 유지 해제


%%
% 피규어 크기 설정 및 축 틱 길이, 폰트 설정
figure('Position', [100, 100, 1000, 800]); % 위치와 크기 설정
ax = gca; % 현재 축 핸들
ax.TickLength = [0.02 0.025]; % 틱 길이 조정
set(ax, 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'FontSize', 20); % 폰트 설정
clim([0 150]);
colormap(jet(41));
h = colorbar;

%ylabel(h, 'Velocity (km/h)','FontName', 'Times New Roman','FontWeight', 'bold', 'FontSize', 20);
ylabel(h, 'Velocity (km/h)','FontName', 'Times New Roman', 'FontSize', 20);
% 전체 트렌드를 나타내는 plot
%plot(cumulativeTime, accumulateE, 'b', 'LineWidth', 2); % 파란색 선, 굵은 선
hold on; % 현재 그래프 유지

% 각 노드의 점을 나타내는 scatter
for i = 1:length(pathNodes) - 1
        currentVelocity = secondPathData(i,2);
        nextVelocity = secondPathData(i+1,2);
        
        avgVelocity = (currentVelocity + nextVelocity) / 2;
        
        % 컬러맵 크기를 41로 지정합니다.
        cmapSize = 41;
        
        % 정규화된 인덱스를 계산합니다.
        normalizedIndex = round((avgVelocity - 1) / 40 * cmapSize) + 1;
        normalizedIndex = max(min(normalizedIndex, cmapSize), 1);
        
        % 컬러맵에서 색상을 가져옵니다.
        color = jet(cmapSize);
        color = color(normalizedIndex, :);
        
        line([sCumulativeTime(i,1), sCumulativeTime(i+1,1)],[sAccumulateE(i,1),sAccumulateE(i+1,1)], 'Color',color , 'LineWidth', 6);
end
%scatter(cumulativeTime, accumulateE, 20, 'r', 'MarkerFaceColor', 'r'); % 빨간색 점, 검은색 테두리, 작은 크기




% 축 레이블 추가
xlabel('Time (s)', 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'FontSize', 20); % X축 레이블
ylabel('Accumulated Energy (kWs)', 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'FontSize', 20); % Y축 레이블

% Y축 틱 값 조정
yticks(0:1000:7000); % 0부터 70까지 10 단위로 틱 설정
yticklabels(arrayfun(@(x) sprintf('%d', x), 0:1000:7000, 'UniformOutput', false)); % 레이블 형식 지정

sFinalTime = sCumulativeTime(end);
sFinalEnergy = sAccumulateE(end);
annotationText = sprintf('Total Time: %.2f s\nAccumulated Energy: %.2f kWs', sFinalTime, sFinalEnergy);

% 텍스트 상자 추가
annotation('textbox', [0.15, 0.8, 0.1, 0.1], 'String', annotationText, ...
    'FontSize', 19, 'FontWeight', 'bold', 'EdgeColor', 'k', 'BackgroundColor', 'white', ...
    'FontName', 'Times New Roman');

hold off; % 그래프 유지 해제


