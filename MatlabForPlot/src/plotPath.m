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