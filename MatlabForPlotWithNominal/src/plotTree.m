function plotTree(node)
    figure;
    
    % Load and display the image
    img = imread("/home/esl/kyuyong/RRTstar/mapImage/9track2Outlined4.png");
    imagesc(img)
    set(gca, 'YDir', 'normal'); % Y축 방향을 일반적인 그래프 방향으로 변경
    set(gca, 'FontName', 'Times New Roman','FontWeight','bold', 'FontSize', 30); % 틱 레이블 글꼴 설정
    set(gca, 'TickLength', [0.02 0.025]); % 틱 라인 길이 변경
    set(gcf, 'Position', [100, 100, 1000, 800]); % 피규어 위치와 크기 설정


    axis image
    %imshow(img, 'InitialMagnification', 'fit');
    hold on;
    colormap(jet(41));

    xlabel('X axis (m)','FontName', 'Times New Roman','FontWeight', 'bold', 'FontSize', 30); % X축 레이블 추가
    ylabel('Y axis (m)','FontName', 'Times New Roman','FontWeight', 'bold', 'FontSize', 30); % Y축 레이블 추가
    
   

    
    %figureTitle = ('PathHeuristic RRT*');
    %title(figureTitle)
    
    lines = collectLines(node);

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
        plot([x1, x2], [y1, y2], 'k', 'LineWidth', 0.01);
    end

    % Plot all nodes
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
