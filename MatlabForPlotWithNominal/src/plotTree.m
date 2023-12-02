function plotTree(node)
    figure;

    % Load and display the image
    img = imread("/home/esl/kyuyong/RRTstar/mapImage/9track2Outlined4.png");

    imshow(img, 'InitialMagnification', 'fit');
    hold on;
    colormap(jet(41));

    % Define the velocity range
    minVelocity = 0;  % Adjust this value based on your data
    maxVelocity = 41;  % Adjust this value based on your data

    % Set the color axis for the velocity range
    clim([minVelocity maxVelocity]);
    h = colorbar;
    
    ylabel(h, 'Velocity');
    % %Define the grid spacing
    % gridSpacing = 10;
    % 
    % %Get the size of the image
    % [rows, cols] = size(img);
    % graynum = 169/255;
    % grayLine = [graynum graynum graynum];
    % % Draw the grid lines
    % for i = 1:gridSpacing:cols
    %     line([i, i], [1, rows], 'Color', grayLine, 'LineWidth', 0.5); % Vertical lines
    % end
    % for j = 1:gridSpacing:rows
    %     line([1, cols], [j, j], 'Color', grayLine, 'LineWidth', 0.5); % Horizontal lines
    % end

    % Plot the tree
    
    %preOrderTraversal(node);

    % Collect line information
    lines = collectLines(node);

    % Plot all lines and nodes
    plotLinesAndNodes(lines);

    
end

function lines = collectLines(node)
    lines = [];

    if isempty(node.children)
        return;
    end

    for i = 1:length(node.children)
        childNode = node.children{i};
        lines = [lines; [node.x, childNode.x, node.y, childNode.y]];
        lines = [lines; collectLines(childNode)]; % 하위 서브트리의 라인 정보 수집
    end
end

function plotLinesAndNodes(lines)
    numLines = size(lines, 1);

    % Plot all lines
    for i = 1:numLines
        lineInfo = lines(i, :);
        x1 = lineInfo(1);
        x2 = lineInfo(2);
        y1 = lineInfo(3);
        y2 = lineInfo(4);
        plot([x1, x2], [y1, y2], 'k', 'LineWidth', 0.1);
    end

     %Plot all nodes
    %scatter(lines(:, 2), lines(:, 4), 4, 'b', 'filled');
end






















function preOrderTraversal(node)
    plotNode(node);
    if isempty(node.children)
        return;
    end
    
    for i = 1:length(node.children)
        childNode = node.children{i};
        plotSteer(node, childNode);
        preOrderTraversal(childNode);
    end
end

function plotNode(node)
    scatter(node.x, node.y, 4, 'b', 'filled'); % 점 크기를 10으로 조정
end

function plotSteer(parentNode, childNode)

    line([childNode.x, parentNode.x], [childNode.y, parentNode.y], 'Color','k' , 'LineWidth', 0.1);
end
