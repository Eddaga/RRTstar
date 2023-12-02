from RRTsubfunc import *
import matplotlib.pyplot as plt
from main import plotMap
from powerCal import *

import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np
def plot_tree(nodes, newNode, mapData):
    plt.clf()
    plotMap(mapData)
    for node in nodes:
        if node.parent is not None:
            plt.scatter(node.x,node.y,s = 10, c = 'b')
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], 'k', linewidth=0.5)
    plt.plot(newNode.x, newNode.y, 'go', label='새 노드')

    current = newNode
    #while current.parent is not None:
#        plt.plot([current.x, current.parent.x], [current.y, current.parent.y], color = 'b', linewidth=1.0)
#        current = current.parent

    # 색상 맵에 대한 레전드 추가

    plt.pause(0.01)


def rrtStar(nodes,stepSize, mapData, scaler, binaryImage):
    hit = 0
    #for _ in range(iterations):
    while True:
        randNode = getRandomNode(mapData)
        nearestNode = getNearestNode(nodes, randNode)
        if nearestNode is not None:
            newNode = getNewNode(nearestNode, randNode, stepSize, scaler,nodes)
            
            # Check if newNode is valid and obstacle-free
            if newNode and isNewNodeObstacleFree(newNode, nearestNode, mapData,  binaryImage):
                nearNodes = getNearNodes(nodes, newNode, stepSize,binaryImage)
                #if len(nearNodes) != 0:
                selectNewParentNode(nearestNode, newNode, nearNodes)
                rewireNearNodes(nearNodes, newNode)
                
                nodes.append(newNode)
                hit = hit+1
                #plot_tree(nodes, newNode, mapData)  # 현재 트리를 플롯
                if hit == 1000:
                    
                    #plot_tree(nodes,newNode,mapData)    
                    return nodes, hit



    
