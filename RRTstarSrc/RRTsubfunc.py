from RRTutils import *
import random
from PIL import Image


#deal with integrize
def getRandomNode(mapData, possibleVelocity):
    mapTotalDots = mapData[0] + mapData[1]
    newNodeCoordinate = random.choice(mapTotalDots)
    randomNode = Node(newNodeCoordinate[0], 
                      newNodeCoordinate[1], 
                      np.random.randint(1, possibleVelocity)) #(1,41))#(0, possibleVelocity)) # Question1. how can i cnofigure possibleVelocity?? 20230807 kyuyong park.
    # 150.0 km/h
    
    return randomNode

# this function is consider for all nodes.
'''def getNearestNode(nodes, randNode):
    nearestNode = min((node for node in nodes if (getTimeSteer(node, randNode) > 0) and (getDistance(node,randNode) > 0)), 
                      key=lambda node: getTimeSteer(node, randNode), default=None)
    return nearestNode'''



def getNearestNode(nodes, randNode):
    nearestNode = None
    minTimeSteer = float('inf')

    for node in nodes:
        if node.parent is None or (node.parent is not None and 135 <= calculateAngle((node.parent.x,node.parent.y),(node.x,node.y),(randNode.x,randNode.y)) <= 180):
            timeSteer = getTimeSteer(node, randNode)
            if timeSteer > 0 and timeSteer < minTimeSteer:
                if getDistance(node,randNode) > 0:
                    nearestNode = node
                    minTimeSteer = timeSteer

    return nearestNode

#deal with integrize
def getNewNode(nearestNode, randNode, stepSize, scaler):
    newNode = Node(nearestNode.x, nearestNode.y, nearestNode.velocity) # create new node and init as dummy value.
    timeSteer = getTimeSteer(randNode, nearestNode)
    degree = 0
    if timeSteer == float('inf'): # which means newNode and nearestNode at same position
        print("asldkfjalskdjfas")
        return False
        '''if nearestNode.parent is None: # if newNode's coordination is at startNode
            return False
        else: # if same coordination with different velocity that is on integer num
            if nearestNode.velocity == randNode.velocity: # if same, don't append
                return False
            else: # else, check degree just return that node.
                print("herererere!!")
                return newNode'''
    # get nearestNode From Real Number
    if nearestNode.parent is None: # if parentNode is nearestNode, it's dont need to think about angle.
        if timeSteer > stepSize:
            acceleration = getPossibleAccelWithoutDegree(randNode,nearestNode)
            deltaVelocity = nearestNode.velocity + acceleration * stepSize # acceleration * domain time = get delta velocity.
            deltaDistance = (deltaVelocity + nearestNode.velocity) / 2 * stepSize # delta velocity + nearestNode's velocity / 2  * domain time -> avg velocity * domain time -> delta distance.
            distance = getDistance(randNode, nearestNode)
            newNode.x += (randNode.x - nearestNode.x) * deltaDistance / distance # dx * ( distance / delta Distance) -> x + delta x
            newNode.y += (randNode.y - nearestNode.y) * deltaDistance / distance # dy * ( distance / delta Distance) -> y + delta y
            newNode.velocity = deltaVelocity
            #print(acceleration)
            newNode = newNodeIntegrization(newNode, scaler, nearestNode, acceleration, stepSize)
        else:
            acceleration = getPossibleAccelWithoutDegree(randNode,nearestNode)
            deltaVelocity = nearestNode.velocity + acceleration * timeSteer # acceleration * domain time = get delta velocity.
            deltaDistance = (deltaVelocity + nearestNode.velocity) / 2 * timeSteer # delta velocity + nearestNode's velocity / 2  * domain time -> avg velocity * domain time -> delta distance.
            distance = getDistance(randNode, nearestNode)
            newNode.x += (randNode.x - nearestNode.x) * deltaDistance / distance # dx * ( distance / delta Distance) -> x + delta x
            newNode.y += (randNode.y - nearestNode.y) * deltaDistance / distance # dy * ( distance / delta Distance) -> y + delta y
            newNode.velocity = deltaVelocity
            newNode = newNodeIntegrization(newNode, scaler, nearestNode, acceleration, stepSize)
            #print(acceleration)
        return newNode
    else:   
        degree = calculateAngle((nearestNode.parent.x, nearestNode.parent.y), (nearestNode.x, nearestNode.y), (randNode.x, randNode.y))
        if degree >= 135 and degree <= 180:
            if timeSteer > stepSize:
                acceleration = getPossibleAccel(randNode,nearestNode, degree)
                deltaVelocity = nearestNode.velocity + acceleration * stepSize # acceleration * domain time = get delta velocity.
                if deltaVelocity <= getPossibleMaxVelocityWithAngle(newNode,degree).velocity:                    
                    deltaDistance = (deltaVelocity + nearestNode.velocity) / 2 * stepSize # delta velocity + nearestNode's velocity / 2  * domain time -> avg velocity * domain time -> delta distance.
                    distance = getDistance(randNode, nearestNode)
                    newNode.x += (randNode.x - nearestNode.x) * deltaDistance / distance # dx * ( distance / delta Distance) -> x + delta x
                    newNode.y += (randNode.y - nearestNode.y) * deltaDistance / distance # dy * ( distance / delta Distance) -> y + delta y
                    newNode.velocity = deltaVelocity
                    #print(acceleration)
                    newNode = newNodeIntegrization(newNode, scaler, nearestNode, acceleration, stepSize)
                    if newNode and  135 > calculateAngle((nearestNode.parent.x, nearestNode.parent.y), (nearestNode.x, nearestNode.y), (newNode.x, newNode.y)):
                        return False
                else:
                    return False
                
            else:
                acceleration = getPossibleAccel(randNode,nearestNode, degree)
                deltaVelocity = nearestNode.velocity + acceleration * timeSteer # acceleration * domain time = get delta velocity.
                if deltaVelocity <= getPossibleMaxVelocityWithAngle(newNode,degree).velocity:                    
                    deltaDistance = (deltaVelocity + nearestNode.velocity) / 2 * timeSteer # delta velocity + nearestNode's velocity / 2  * domain time -> avg velocity * domain time -> delta distance.
                    distance = getDistance(randNode, nearestNode)
                    newNode.x += (randNode.x - nearestNode.x) * deltaDistance / distance # dx * ( distance / delta Distance) -> x + delta x
                    newNode.y += (randNode.y - nearestNode.y) * deltaDistance / distance # dy * ( distance / delta Distance) -> y + delta y
                    newNode.velocity = deltaVelocity
                    newNode = newNodeIntegrization(newNode, scaler, nearestNode, acceleration, stepSize)
                    if newNode and 135 > calculateAngle((nearestNode.parent.x, nearestNode.parent.y), (nearestNode.x, nearestNode.y), (newNode.x, newNode.y)):
                        return False
                else:
                    return False
                #print(acceleration)
            return newNode
        else:
            return False


def isNearNodeToNewNodeAnglePossible(child, parent):
    grandparent = parent.parent
    if (135 <= calculateAngle((grandparent.x,grandparent.y),(parent.x, parent.y),(child.x, child.y)) < 180):
            
        return True
    else:
        
        return False

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
        if getTimeSteer(node, newNode) < stepSize:
            # 두 노드 사이의 유클리드 거리 계산
            euclidean_distance = getDistance(node, newNode)
            if euclidean_distance > distance_threshold and (not isNodeSteerOnObstacle(node, newNode,mapPath)) \
                and isNodeAccelOk(node, newNode) :
                
                nearNodes.append(node)
    return nearNodes
# add code which consider radius node.(after add grid options..?)

    
#deal with integrize
def selectNewParentNode(nearestNode, newNode, nearNodes):
    minCost = nearestNode.cost + getTimeSteer(nearestNode, newNode)
    minNode = nearestNode

    for nearNode in nearNodes:
        if nearNode.parent is None:
            tempCost = nearNode.cost + getTimeSteer(nearNode, newNode)
            if tempCost < minCost:
                minCost = tempCost
                minNode = nearNode
        if nearNode.parent is not None:
            degree = calculateAngle((nearNode.parent.x,nearNode.parent.y),(nearNode.x,nearNode.y),(newNode.x,newNode.y))
            if 135 <= degree <= 180:
                tempNewNode = fitNewNodeVelocity(nearNode, newNode)
                if isNodeAccelOk(nearNode, tempNewNode): 
                    tempCost = nearNode.cost + getTimeSteer(nearNode, tempNewNode)
                    if tempCost < minCost:
                        minCost = tempCost
                        minNode = nearNode
                        newNode.velocity = tempNewNode.velocity

    newNode.cost = minCost
    if newNode.parent:
        newNode.parent.children.remove(newNode)
    newNode.parent = minNode
    minNode.children.append(newNode)
    updateChildCost(newNode, newNode.cost)

## have to fix this func
def rewireNearNodes(nearNodes, newNode, start):
    for nearNode in nearNodes:
        if getDistance(start,nearNode) > 0:
            '''if newNode.parent.parent is None:
                print("hello!")
                tempCostWithNewNode = newNode.cost + getTimeSteer(newNode, nearNode)
                if tempCostWithNewNode < nearNode.cost:
                # Update the parent of the nearNode
                    if nearNode.parent:
                        nearNode.parent.children.remove(nearNode)  # Remove nearNode from the old parent's children list
                    nearNode.parent = newNode
                    newNode.children.append(nearNode)  # Add nearNode to the new parent's children list

                    # Update the cost of nearNode and recursively update the costs of all its descendants
                    nearNode.cost = tempCostWithNewNode
                    updateChildCost(nearNode, tempCostWithNewNode)'''

            degree = calculateAngle((newNode.parent.x,newNode.parent.y),(newNode.x,newNode.y),(nearNode.x,nearNode.y))
            if 135 <= degree <= 180 and isNearNodeVelocityPossible(nearNode,newNode, degree):
                tempCostWithNewNode = newNode.cost + getTimeSteer(newNode, nearNode)
                if tempCostWithNewNode < nearNode.cost:
                    if isNodeAccelOk(nearNode, newNode): 
                        # Update the parent of the nearNode
                        if nearNode.parent:
                            nearNode.parent.children.remove(nearNode)  # Remove nearNode from the old parent's children list
                        nearNode.parent = newNode
                        newNode.children.append(nearNode)  # Add nearNode to the new parent's children list

                        # Update the cost of nearNode and recursively update the costs of all its descendants
                        nearNode.cost = tempCostWithNewNode
                        updateChildCost(nearNode, tempCostWithNewNode)



def isGoalReached(newNode, goal,threshold):
    return getDistance(newNode, goal) < threshold

