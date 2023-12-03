function pathNodes = getPathNodeAndSave(startNode, goalNode,fileNum) 
    if ~isempty(goalNode)
        pathNodes = traceBackPath(goalNode, startNode);
%        plotPath(pathNodes);
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



