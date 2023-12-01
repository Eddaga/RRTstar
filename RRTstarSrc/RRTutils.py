import numpy as np
import pandas as pd
from bresenham import bresenham

class Node:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.cost = 0
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

    intNodeInTime = [node for node in intNodes if (getTimeSteer(node, nearestNode) < stepSize) and (getDistance(node,nearestNode) > 0)]

    if not intNodeInTime:
        return False
    else:
        newNode = min(intNodeInTime, key=lambda node: getTimeSteer(node, newNode))
        return newNode

def getPossibleMaxVelocityWithAngle(child, degree):
    tempNode = Node(child.x, child.y, child.velocity)
    
    if degree >= 135 and degree <= 180:
        # degree가 120도에서 180도 사이인 경우
        # 비율을 계산해서 반환 (120도는 10%, 180도는 100%)
        ratio = (degree - 135) / 45  # 120도는 10%, 180도는 100%
        tempNode.velocity = 3 + ratio * 38

        return tempNode
    else:

        # 그 외의 경우에는 None 또는 다른 예외 처리를 수행
        return False  # 또는 예외를 발생시킴
    
def getPossibleAccelWithoutDegree(newNode,nearestNode):
    maxAccel = 3.026 #100km/h/3.6/9.18s = 3.026m/(s^2)
    newAccel = (newNode.velocity - nearestNode.velocity) / getTimeSteer(newNode, nearestNode)

    if newAccel < maxAccel:
        
        return newAccel
        
    else:
        
        return maxAccel

def getPossibleAccel(newNode,nearestNode,degree):


    maxAccel = 3.026 #100km/h/3.6/9.18s = 3.026m/(s^2)
    newAccel = (newNode.velocity - nearestNode.velocity) / getTimeSteer(newNode, nearestNode)
    accelToUse = newAccel

    if nearestNode.parent is not None:
        tempNodeForWithAngle = getPossibleMaxVelocityWithAngle(newNode, degree)
        newAccelWithPossibleVelocity = (tempNodeForWithAngle.velocity - nearestNode.velocity) / getTimeSteer(tempNodeForWithAngle, nearestNode)
        accelToUse = max(newAccelWithPossibleVelocity,newAccel)

    if accelToUse < maxAccel:
        
        return accelToUse
        
    else:
        
        return maxAccel

def isNodeAccelOk(primaryNode, followNode):
    maxAccel = 3.026
    newAccel = (followNode.velocity - primaryNode.velocity) / getTimeSteer(followNode, primaryNode)

    
    if (0 - maxAccel) < newAccel < maxAccel:
        
        return True
    else:
        
        return False


def calculateSignedAngle(p1, p2, p3):
    """
    Calculate the signed angle at p2 formed by the line segments p1-p2 and p2-p3.
    
    Args:
    p1, p2, p3 (tuples/lists): Coordinates of the three points (x, y).

    Returns:
    float: Signed angle at p2 in degrees. Positive if the angle is counterclockwise,
           negative if clockwise.
    """
    # Convert points to numpy arrays for vector operations
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    # Calculate vectors
    v1 = p1 - p2
    v2 = p3 - p2

    # Calculate the angle using the dot product and arccosine function
    angle_radians = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0))

    # Calculate the cross product to determine the direction of the angle
    cross_product = np.cross(v1, v2)

    # Convert to degrees and apply sign based on the direction
    if cross_product > 0:
        # Counterclockwise direction
        angle_degrees = np.degrees(angle_radians)
    else:
        # Clockwise direction
        angle_degrees = -np.degrees(angle_radians)

    return angle_degrees
    
import numpy as np

def calculateAngle(p1, p2, p3):
    """
    Calculate the angle at p2 formed by the line segments p1-p2 and p2-p3.
    
    Args:
    p1, p2, p3 (tuples/lists): Coordinates of the three points (x, y).

    Returns:
    float: Angle at p2 in degrees.
    """
    # Convert points to numpy arrays for vector operations
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    # Calculate vectors
    v1 = p1 - p2
    v2 = p3 - p2

    # Calculate the angle using the dot product and arccosine function
    angle_radians = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    # Convert to degrees
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees

def fitNewNodeVelocity (nearNode, newNode):
    
    degree = calculateAngle((nearNode.parent.x,nearNode.parent.y),(nearNode.x,nearNode.y),(newNode.x,newNode.y))
    tempNode = getPossibleMaxVelocityWithAngle(newNode,degree)
    if newNode.velocity < tempNode.velocity:
        tempNode = newNode
    return tempNode

def isNearNodeVelocityPossible (nearNode,newNode, degree):
    tempNode = getPossibleMaxVelocityWithAngle(nearNode,degree)
    if tempNode and tempNode.velocity >= nearNode.velocity:
        for child in nearNode.children:
            degreeForChild = calculateAngle((newNode.x,newNode.y),(nearNode.x,nearNode.y),(child.x,child.y))
            tempNodeForChild = getPossibleMaxVelocityWithAngle(child,degreeForChild)
            if not tempNodeForChild:
                return False
            if tempNodeForChild.velocity < child.velocity:
                return False
        return True
    else:
        return False

def createLinePixels(x0, y0, x1, y1):
    """ Create a binary array representing the line between two points. """
    points = list(bresenham(x0, y0, x1, y1))
    
    
    return points

def updateChildCost(node, cost):
    # Recursively update the cost of the node and all its descendants
    for child in node.children:
        child.cost = cost + getTimeSteer(node, child)
        
        updateChildCost(child, child.cost)



def save_to_excel(tree, map_data, scaler, fileNum):
    # Convert tree data to a DataFrame
    fileName = "/home/esl/kyuyong/RRTstar/result4/" + str(fileNum) + "output.xlsx"
    
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
