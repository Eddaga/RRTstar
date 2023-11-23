function getPathNodeAndSave(startNode, goalNode,fileNum) 
    if ~isempty(goalNode)
        pathNodes = traceBackPath(goalNode, startNode);
        plotPath(pathNodes);
        filePath = "/home/esl/kyuyong/RRTstar/foundPath/" + num2str(fileNum) + "pathNodes.xlsx";
        saveNodesToExcel(pathNodes,filePath);
    else
        disp('No suitable goal node found.');
    end
end

function pathNodes = traceBackPath(goalNode, startNode)
    currentNode = goalNode;
    pathNodes = {};
    

    while ~isempty(currentNode) && currentNode ~= startNode

        pathNodes{end + 1} = currentNode;
        currentNode = currentNode.parent; % Assuming each node has a 'parent' property
        currentNode = currentNode{1};
    end
    pathNodes{end + 1} = startNode; % Add the start node

    % Reverse the order to start from the startNode
    pathNodes = fliplr(pathNodes);
end

function plotPath(pathNodes)
    for i = 1:length(pathNodes) - 1
        currentNode = pathNodes{i};
        
        nextNode = pathNodes{i + 1};
        nextNode = nextNode;
        plotSteer(currentNode, nextNode); % Use your existing plotSteer function
        %plotNode(currentNode); % Use your existing plotNode function
    end
    %plotNode(pathNodes{end}); % Plot the last node
    hold off
end

function saveNodesToExcel(pathNodes, fileName)
    % Extract node details
    a = pathNodes;
    nodeDetails = zeros(length(pathNodes),4);
    for i = 1:length(pathNodes)
        nodeDetails(i,:) = [a{1,i}.x ...
                          a{1,i}.y ...
                          a{1,i}.velocity, ...
                          a{1,i}.cost];
    end
    
    % Convert to table
    nodeTable = array2table(nodeDetails, 'VariableNames', {'X', 'Y', 'Velocity', 'Cost'});

    % Write to Excel file
    
    writetable(nodeTable, fileName);
end

function plotSteer(currentNode, nextNode)

    avgVelocity = (currentNode.velocity + nextNode.velocity) / 2;

    % 컬러맵 크기를 41로 지정합니다.
    cmapSize = 41;

    % 정규화된 인덱스를 계산합니다.
    normalizedIndex = round((avgVelocity - 1) / 40 * cmapSize) + 1;
    normalizedIndex = max(min(normalizedIndex, cmapSize), 1);

    % 컬러맵에서 색상을 가져옵니다.
    color = jet(cmapSize);
    color = color(normalizedIndex, :);

    %선을 그립니다.
    line([currentNode.x, nextNode.x], [currentNode.y, nextNode.y], 'Color',color , 'LineWidth', 3);
end

function plotNode(node)
    scatter(node.x, node.y, 50, 'red', 'filled','d'); % 점 크기를 10으로 조정
end

