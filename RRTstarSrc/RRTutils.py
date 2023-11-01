import numpy as np

class Node:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.cost = 0
        self.parent = None

def getDistance(node1, node2):
    return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

def getTimeSteer(node1, node2):
    if node1.x == node2.x and node1.y == node2.y:
        return float('inf')
    return getDistance(node1, node2) / ( (node1.velocity + node2.velocity) / 2 )

def newNodeIntegrization(newNode, scaler, nearestNode, acceleration, stepSize):
    ddX = int(np.floor(newNode.x / scaler) * scaler)
    ddY = int(np.floor(newNode.y / scaler) * scaler)

    udX = int(np.ceil(newNode.x / scaler) * scaler)
    udY = int(np.floor(newNode.y / scaler) * scaler)

    duX = int(np.floor(newNode.x / scaler) * scaler)
    duY = int(np.ceil(newNode.y / scaler) * scaler)

    uuX = int(np.ceil(newNode.x / scaler) * scaler)
    uuY = int(np.ceil(newNode.y / scaler) * scaler)

    # V^2 = (V_0)^2 + 2as //
    ddDistance = np.sqrt((nearestNode.x - ddX) ** 2 + (nearestNode.y - ddY) ** 2) 
    ddv = int(round(np.sqrt(pow(nearestNode.velocity,2) + (2*acceleration * ddDistance))))
    dd = Node(ddX,ddY,ddv)       
            
    udDistance = np.sqrt((nearestNode.x - udX) ** 2 + (nearestNode.y - udY) ** 2)
    udv = int(round(np.sqrt(pow(nearestNode.velocity,2) + (2*acceleration * udDistance))))
    ud = Node(udX,udY,udv)
    
    duDistance = np.sqrt((nearestNode.x - duX) ** 2 + (nearestNode.y - duY) ** 2)
    duv = int(round(np.sqrt(pow(nearestNode.velocity,2) + (2*acceleration * duDistance))))
    du = Node(duX,duY,duv)
    
    uuDistance = np.sqrt((nearestNode.x - uuX) ** 2 + (nearestNode.y - uuY) ** 2)
    uuv = int(round(np.sqrt(pow(nearestNode.velocity,2) + (2*acceleration * uuDistance))))
    uu = Node(uuX,uuY,uuv)
  
    # 4점 중 inside인 점 찾기
    intNodes = [dd, ud, du, uu]
    intNodeInTime = [intNode for intNode in intNodes if getTimeSteer(intNode, nearestNode) < stepSize ]
    
    # 만약에 없으면, newNode 없음! return False!
    if not intNodeInTime:
        return False
    
    # inside 인 점 중에서 newNode랑 가장 가까운 점 -> newNode
    else:
        newNode = min(intNodeInTime, key=lambda node: getTimeSteer(node, newNode))
        return newNode