treenum = 100000;


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
    %%
    getPathNodeAndSave(nodes{1}, nodeNearGoal,treenum);
    xMax = 900;
    yMin = 520;

    xMin = 875;
    yMax = 549;
    rectangle('Position', [xMin, yMin, xMax-xMin, yMax-yMin], 'EdgeColor', 'r', 'FaceColor', 'r', 'LineWidth', 2);

