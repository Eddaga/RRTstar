import numpy as np
import pandas as pd
from bresenham import bresenham

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = 0
        self.parent = None
        self.children = []


def getDistance(node1, node2):
    return np.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def newNodeIntegrization(newNode, scaler, nearestNode, stepSize):
    coordinates = [
        (int(np.floor(newNode.x / scaler) * scaler), int(np.floor(newNode.y / scaler) * scaler)),
        (int(np.ceil(newNode.x / scaler) * scaler), int(np.floor(newNode.y / scaler) * scaler)),
        (int(np.floor(newNode.x / scaler) * scaler), int(np.ceil(newNode.y / scaler) * scaler)),
        (int(np.ceil(newNode.x / scaler) * scaler), int(np.ceil(newNode.y / scaler) * scaler))
    ]

    
    intNodes = []
    for x, y in coordinates:
        candidateNode = Node(x, y)

        distance = getDistance(candidateNode, nearestNode)
        if distance <= stepSize:
            intNodes.append(candidateNode)

    if not intNodes:
        return False
    newNode = min(intNodes, key=lambda node: getDistance(node, newNode))
    return newNode

def getCost(node1, node2):
    return getDistance(node1, node2)


def createLinePixels(x0, y0, x1, y1):
    """ Create a binary array representing the line between two points. """
    points = list(bresenham(x0, y0, x1, y1))
    return points



def save_to_excel(tree, map_data, scaler, fileNum):
    # Convert tree data to a DataFrame
    fileName = "/home/esl/kyuyong/RRTstar/resultNormalRRT/" + str(fileNum) + "output.xlsx"
    
    tree_data = []
    for index, node in enumerate(tree):
        children_indices = '; '.join([str(tree.index(child)) for child in node.children])
        tree_data.append({
            'id': index,
            'x': node.x,
            'y': node.y,
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
