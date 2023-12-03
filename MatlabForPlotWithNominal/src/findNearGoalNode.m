function smallestCostNodeNearGoal = findNearGoalNode(nodes)
    % Define the area limits
    
    xMax = 1000;
    yMin = 530;

    xMin = 865;
    yMax = 560;

    % Initialize variables
    smallestCost = Inf;
    smallestCostNodeNearGoal = [];
    

    % 여기서 'Position'은 사각형의 위치와 크기를 지정합니다.
    % Iterate through all nodes
    for i = 1:length(nodes)
        node = nodes{i};
        % Check if the node is within the specified area
        if node.x >= xMin && node.x <= xMax && node.y >= yMin && node.y <= yMax
            % Check if this node has the smallest cost so far
            if node.cost < smallestCost
                smallestCost = node.cost;
                smallestCostNodeNearGoal = node;
            end
        end
    end

    % Check if a node was found
    if isempty(smallestCostNodeNearGoal)
        disp('No node found in the specified area.');
    else
        disp(['Smallest cost node found with cost: ', num2str(smallestCost)]);
    end
end