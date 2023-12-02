function nodes = nodeTranslator(data)

    % Create an array to store TreeNode objects
    nodes = cell(height(data), 1);

    % First pass: Create TreeNode objects
    
    
    
    for i = 1:height(data)
        row = data(i, :);
        nodes{i} = TreeNode(row.x, row.y, row.cost, row.parent_id);
    end

    for i = 2:height(data)
        row = data(i, :);
        nodes{i}.addParent(nodes{row.parent_id+1});
    end


    % Second pass: Set up child-parent relationships
    for i = 1:height(data)
        row = data(i, :);
        if ~ismissing(row.children_ids) && ~isempty(row.children_ids)
            childrenIds = strsplit(char(row.children_ids), ';');

            for j = 1:length(childrenIds)
                childId = str2double(childrenIds{j});
                nodes{i}.addChild(nodes{childId+1}); % Adjust index if necessary
            end
        end
    end

end