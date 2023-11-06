from RRTutils import *
import random


#deal with integrize
def getRandomNode(mapData, possibleVelocity):
    mapTotalDots = mapData[0] + mapData[1]
    newNodeCoordinate = random.choice(mapTotalDots)
    randomNode = Node(newNodeCoordinate[0], 
                      newNodeCoordinate[1], 
                      np.random.randint(0,40))#(0, possibleVelocity)) # Question1. how can i cnofigure possibleVelocity?? 20230807 kyuyong park.
    # 150.0 km/h
    return randomNode

# this function is consider for all nodes.
def getNearestNode(nodes, randNode):
    nearestNode = min((node for node in nodes if getTimeSteer(node, randNode) > 0), 
                      key=lambda node: getTimeSteer(node, randNode), default=None)
    return nearestNode

#deal with integrize
def getNewNode(nearestNode, randNode, stepSize, scaler):
    newNode = Node(nearestNode.x, nearestNode.y, nearestNode.velocity) # create new node and init as dummy value.
    timeSteer = getTimeSteer(randNode, nearestNode)
    
    if timeSteer == float('inf'):
        return False
    # get nearestNode From Real Number
    if timeSteer > stepSize:
        acceleration = (randNode.velocity - nearestNode.velocity) / timeSteer # Accel = (V_1 - V_2)/ time, so calculation is (nearestNodeVelocity - randNodeVelocity) / time, to move from nearsetNode to randNode.
        deltaVelocity = nearestNode.velocity + acceleration * stepSize # acceleration * domain time = get delta velocity.
        deltaDistance = (deltaVelocity + nearestNode.velocity) / 2 * stepSize # delta velocity + nearestNode's velocity / 2  * domain time -> avg velocity * domain time -> delta distance.
        distance = getDistance(randNode, nearestNode)
        newNode.x += (randNode.x - nearestNode.x) * deltaDistance / distance # dx * ( distance / delta Distance) -> x + delta x
        newNode.y += (randNode.y - nearestNode.y) * deltaDistance / distance # dy * ( distance / delta Distance) -> y + delta y
        newNode.velocity = deltaVelocity
        
    #change it to integer            
        newNode = newNodeIntegrization(newNode, scaler, nearestNode, acceleration, stepSize)
        
    else:
        newNode.x = randNode.x
        newNode.y = randNode.y
        newNode.velocity = randNode.velocity
        #print("<case, ",newNode.x," ",newNode.y," ",newNode.velocity)
    return newNode

#deal with integrize
def isNodeOnObstacle(newNode, MapData):
    if (newNode.x, newNode.y) in MapData[1]:
        
        return False
    else:
        #print(newNode.x,newNode.y,"out")
        return True

#deal with integrize
def isNodeSteerOnObstacle(node1, node2, MapData, scaler):
    x1, y1 = node1.x, node1.y
    x2, y2 = node2.x, node2.y
    distance = getDistance(node1, node2)
    
    num_steps = int(distance / scaler)
    
    for i in range(num_steps + 1):
        x = x1 + i * scaler * (x2 - x1) / distance
        y = y1 + i * scaler * (y2 - y1) / distance
        
        x, y = round(x), round(y)
        print(x,y)
        if (x, y) in MapData[0]:  # MapData[1] is white
            return True
    
    return False


#deal with integrize
def isNewNodeObstacleFree(newNode, nearestNode, mapData, scaler):
    if isNodeOnObstacle(newNode, mapData):
        
        return False
    if isNodeSteerOnObstacle(newNode, nearestNode, mapData, scaler):
        
        return False
    else:
        
        return True

# this function is consider for all nodes.
def getNearNodes(nodes, newNode, stepSize, distance_threshold=0):
    nearNodes = []
    for node in nodes:
        # 시간 스티어를 통해 노드가 주어진 범위 내에 있는지 확인
        if getTimeSteer(node, newNode) < stepSize:
            # 두 노드 사이의 유클리드 거리 계산
            euclidean_distance = getDistance(node, newNode)
            if euclidean_distance > distance_threshold:
                nearNodes.append(node)
    return nearNodes
# add code which consider radius node.(after add grid options..?)

#deal with integrize
def selectNewParentNode(nearestNode, newNode, nearNodes):
    minCost = nearestNode.cost + getTimeSteer(nearestNode, newNode)
    
    minNode = nearestNode
    for nearNode in nearNodes:
        tempCost = nearNode.cost + getTimeSteer(nearNode, newNode)
        if tempCost < minCost:
            minCost = tempCost
            minNode = nearNode
    newNode.cost = minCost
    newNode.parent = minNode

def rewireNearNodes(nearNodes, newNode):
    for nearNode in nearNodes:
        tempCostWithNewNode = newNode.cost + getTimeSteer(newNode, nearNode)
        if tempCostWithNewNode < nearNode.cost:
                nearNode.cost = tempCostWithNewNode
                nearNode.parent = newNode

def isGoalReached(newNode, goal,threshold):
    return getDistance(newNode, goal) < threshold

