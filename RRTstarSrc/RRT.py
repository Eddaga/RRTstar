from RRTsubfunc import *
import matplotlib.pyplot as plt





def rrtStar(nodes, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, goal, threshold):

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
        
    else:
        print("Goal not reached within the specified iterations.")
      


    return nodes


    
