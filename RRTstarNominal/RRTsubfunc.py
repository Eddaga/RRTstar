from RRTutils import *
import random
from PIL import Image


#deal with integrize
def getRandomNode(mapData):
    mapTotalDots = mapData[0] + mapData[1]
    newNodeCoordinate = random.choice(mapData[0])
    randomNode = Node(newNodeCoordinate[0], newNodeCoordinate[1])
    return randomNode

def getNearestNode(nodes, randNode):
    nearestNode = None
    minDistance = float('inf')
    for node in nodes:
        tempDistance = getDistance(node,randNode)
        if 0 < tempDistance < minDistance:
            nearestNode = node
            minDistance = tempDistance

    return nearestNode

#deal with integrize
def getNewNode(nearestNode, randNode, stepSize, scaler, nodes):
    newNode = Node(nearestNode.x, nearestNode.y) # create new node and init as dummy value.
    distance = getDistance(randNode, nearestNode)
 
    if distance > stepSize:
        newNode.x += (randNode.x - nearestNode.x) * stepSize / distance # dx * ( distance / delta Distance) -> x + delta x
        newNode.y += (randNode.y - nearestNode.y) * stepSize / distance # dy * ( distance / delta Distance) -> y + delta y
        newNode = newNodeIntegrization(newNode, scaler, nearestNode, stepSize)
    else:
        newNode = randNode
 
    return newNode

#deal with integrize
def isNodeOnObstacle(newNode, MapData):
    if (newNode.x, newNode.y) in MapData[0]:
        
        return False
    else:

        return True

#deal with integrize


def isNodeSteerOnObstacle(node1, node2, binaryImage):
    """ Check if the path between two nodes crosses an obstacle using AND operation. """
    # Load the image and convert it to binary scale
    
    
    # Create line pixels without including the start and end points
    linePixels = createLinePixels(node1.x, node1.y, node2.x, node2.y)
    
    for x, y in linePixels:
        if binaryImage.getpixel((x, y)) != 1:  # Check if the value at (x, y) is 1
            
            return True
    
    return False

#deal with integrize
def isNewNodeObstacleFree(newNode, nearestNode, mapData, binaryImage):
    
    if isNodeOnObstacle(newNode, mapData):
        
        return False
    if isNodeSteerOnObstacle(newNode, nearestNode, binaryImage):
        
        return False
    else:
        
        return True

# this function is consider for all nodes.
def getNearNodes(nodes, newNode, stepSize,mapPath, distance_threshold=0):
    nearNodes = []
    for node in nodes:
        # 시간 스티어를 통해 노드가 주어진 범위 내에 있는지 확인
        if getDistance(node, newNode) < stepSize:
            # 두 노드 사이의 유클리드 거리 계산
            euclidean_distance = getDistance(node, newNode)
            if euclidean_distance > distance_threshold and (not isNodeSteerOnObstacle(node, newNode,mapPath)):
                nearNodes.append(node)
    return nearNodes
# add code which consider radius node.(after add grid options..?)

    
#deal with integrize
def selectNewParentNode(nearestNode, newNode, nearNodes):
    minCost = nearestNode.cost + getCost(nearestNode, newNode)
    minNode = nearestNode

    for nearNode in nearNodes:
        tempCost = nearNode.cost + getCost(nearNode, newNode)
        if tempCost < minCost:
            minCost = tempCost
            minNode = nearNode

    newNode.cost = minCost
    if newNode.parent:
        newNode.parent.children.remove(newNode)
    newNode.parent = minNode
    minNode.children.append(newNode)
    updateChildCost(newNode, newNode.cost)

## have to fix this func
def rewireNearNodes(nearNodes, newNode):
    for nearNode in nearNodes:
        tempCostWithNewNode = newNode.cost + getCost(newNode, nearNode)
        if tempCostWithNewNode < nearNode.cost:
            if nearNode.parent:
                nearNode.parent.children.remove(nearNode)  # Remove nearNode from the old parent's children list
            nearNode.parent = newNode
            newNode.children.append(nearNode)  # Add nearNode to the new parent's children list
            nearNode.cost = tempCostWithNewNode
            updateChildCost(nearNode, tempCostWithNewNode)

def updateChildCost(node, cost):
    # Recursively update the cost of the node and all its descendants
    for child in node.children:
        child.cost = cost + getDistance(node, child)
        
        updateChildCost(child, child.cost)

