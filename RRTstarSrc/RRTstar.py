'''ALGORITHM RRT*
V ← {xinit}; E← {}, T ← (V,E);
1. for i = 0 to i = N do
2.	xrand ← RANDOM_NODE(Xfree)
3.	xnearest ← NEAREST_NODE(xrand)
4.	xnew ← CONF_NEW_NODE(xnearest, xrand,dstepsize)
5.	if(OBSTACLE_FREE(xnew, xnearest,Xobstacle)) then
6.		Xnear ← Near(T, xnew, radious)
7.		SELECT_PARENT(Xnear,xnew,E)
8.		REWIRE(Xnear,xnew,E);
9.		V ← V ∪ {xnew);
10.	end
11.endfor
12.return T =(V,E)
'''

from RRTsubfunc import *


def rrtStar(nodes, start, goal, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, threshold):
    if ~nodes:
        nodes = [start]
    else:
        print("use exist Tree\r\n")

    for _ in range(iterations):
        randNode = getRandomNode(mapMaxSize, possibleVelocity)
        nearestNode = getNearestNode(nodes, randNode)
        newNode = getNewNode(nearestNode, randNode, stepSize, scaler)
        
        # Check if newNode is valid and obstacle-free
        if newNode and isNewNodeObstacleFree(newNode, nearestNode, mapData, scaler):
            nearNodes = getNearNodes(nodes, newNode, stepSize)
            selectNewParentNode(nearestNode, newNode, nearNodes)
            rewireNearNodes(nearNodes, newNode)
            nodes.append(newNode)
            
            # Check if the goal is reached
            if isGoalReached(newNode, goal, threshold):
                print("Goal reached!")
                return nodes, newNode  # or you might return a path, depending on your use case
            
    print("Goal not reached within the specified iterations.")
    return nodes, False  # or you might return None or an empty path, depending on your use case    




def rrtStar(nodes, start, goal, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, threshold):
    if nodes:
        nodes = [start]
    for _ in range(iterations):
        randNode = getRandomNode(mapMaxSize, possibleVelocity)
        nearestNode = getNearestNode(nodes, randNode)
        newNode = getNewNode(nearestNode, randNode, stepSize, scaler)
        
        # Check if newNode is valid and obstacle-free
        if newNode and isNewNodeObstacleFree(newNode, nearestNode, mapData, scaler):
            nearNodes = getNearNodes(nodes, newNode, stepSize)
            selectNewParentNode(nearestNode, newNode, nearNodes)
            rewireNearNodes(nearNodes, newNode)
            nodes.append(newNode)
            
            # Check if the goal is reached
            if isGoalReached(newNode, goal, threshold):
                print("Goal reached!")
                return nodes, newNode  # or you might return a path, depending on your use case
        
    print("Goal not reached within the specified iterations.")
    return nodes, False  # or you might return None or an empty path, depending on your use case   


    
