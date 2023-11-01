from RRTsubfunc import *

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


    
