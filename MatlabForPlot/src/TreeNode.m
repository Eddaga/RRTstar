classdef TreeNode < handle
    properties
        x
        y
        velocity
        cost
        parent_id
        parent
        children
    end
    
    methods
        function obj = TreeNode(x,y,velocity,cost,parent_id)
            obj.x = x;
            obj.y = y;
            obj.velocity = velocity;
            obj.cost = cost;
            obj.parent_id = parent_id;
            obj.parent; 
            
            obj.children = {};
            
        end
        
        function addChild(obj, child)
            obj.children{end+1} = child;
        end

        function addParent(obj, parent)
            obj.parent{end+1} = parent;
        end
    end
end