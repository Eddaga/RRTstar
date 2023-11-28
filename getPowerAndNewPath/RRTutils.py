import numpy as np
import pandas as pd


class Node:
    def __init__(self, x, y, velocity, cost):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.cost = cost
        self.parent = None
        self.children = []

def getDistance(node1, node2):
    return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

def getTimeSteer(node1, node2):
    if node1.x == node2.x and node1.y == node2.y:
        return float('inf')
    return getDistance(node1, node2) / ( (node1.velocity + node2.velocity) / 2 )

def calculateDistanceAndVelocity(x, y, nearestNode, acceleration):
    distance = np.sqrt((nearestNode.x - x) ** 2 + (nearestNode.y - y) ** 2)
    if np.isnan(distance) or distance < 0:
        return None, None

    velocity_squared = nearestNode.velocity**2 + 2 * acceleration * distance
    if velocity_squared < 0:
        return None, None

    velocity = int(round(np.sqrt(velocity_squared)))
    return distance, velocity

def newNodeIntegrization(newNode, scaler, nearestNode, acceleration, stepSize):
    coordinates = [
        (int(np.floor(newNode.x / scaler) * scaler), int(np.floor(newNode.y / scaler) * scaler)),
        (int(np.ceil(newNode.x / scaler) * scaler), int(np.floor(newNode.y / scaler) * scaler)),
        (int(np.floor(newNode.x / scaler) * scaler), int(np.ceil(newNode.y / scaler) * scaler)),
        (int(np.ceil(newNode.x / scaler) * scaler), int(np.ceil(newNode.y / scaler) * scaler))
    ]

    intNodes = []
    for x, y in coordinates:
        distance, velocity = calculateDistanceAndVelocity(x, y, nearestNode, acceleration)
        if distance is not None and velocity is not None:
            intNodes.append(Node(x, y, velocity))

    intNodeInTime = [node for node in intNodes if getTimeSteer(node, nearestNode) < stepSize]

    if not intNodeInTime:
        return False
    else:
        newNode = min(intNodeInTime, key=lambda node: getTimeSteer(node, newNode))
        return newNode

'''def newNodeIntegrization(newNode, scaler, nearestNode, acceleration, stepSize):
    
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
        
        return newNode'''


def save_to_excel(tree, map_data, scaler, fileNum):
    # Convert tree data to a DataFrame
    fileName = "/home/esl/kyuyong/RRTstar/result/" + str(fileNum) + "output.xlsx"
    
    tree_data = []
    for index, node in enumerate(tree):
        children_indices = '; '.join([str(tree.index(child)) for child in node.children])
        tree_data.append({
            'id': index,
            'x': node.x,
            'y': node.y,
            'velocity': node.velocity,
            'cost': node.cost,
            'parent_id': tree.index(node.parent) if node.parent else None,
            'children_ids': children_indices
        })
    tree_df = pd.DataFrame(tree_data)

    # Convert map data to a DataFrame
    blackList, whiteList = map_data
    map_black_df = pd.DataFrame(blackList, columns=['x', 'y'])
    map_white_df = pd.DataFrame(whiteList, columns=['x', 'y'])

    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(fileName, engine='openpyxl') as writer:
        tree_df.to_excel(writer, sheet_name='Tree Data')
        map_black_df.to_excel(writer, sheet_name='Map Black Data')
        map_white_df.to_excel(writer, sheet_name='Map White Data')
        # Save scaler as a separate sheet
        scaler_df = pd.DataFrame([{'scaler': scaler}])
        scaler_df.to_excel(writer, sheet_name='Scaler Data')
