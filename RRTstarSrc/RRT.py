from RRTsubfunc import *
import matplotlib.pyplot as plt
from main import plotMap
from powerCal import *

import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np
def plot_tree(nodes, newNode, mapData, goal):
    plt.clf()
    plotMap(mapData)
    for node in nodes:
        if node.parent is not None:
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], 'b-', linewidth=0.5)
    plt.plot(newNode.x, newNode.y, 'go', label='새 노드')

    # 색상 맵 생성
    cmap = cm.get_cmap('viridis', 41)  # 속도 범위에 따른 색상 맵 생성
    norm = colors.Normalize(vmin=0, vmax=41)  # 속도 범위 정규화

    current = newNode
    while current.parent is not None:
        # 현재 노드의 속도에 따라 색상 결정
        color = cmap(int(current.velocity))

        plt.plot([current.x, current.parent.x], [current.y, current.parent.y], color=color, linewidth=1.0)
        current = current.parent

    # 색상 맵에 대한 레전드 추가

    plt.pause(0.01)


def rrtStar(nodes, start, stepSize, possibleVelocity, mapData, scaler, goal, threshold,binaryImage):
    hit = 0
    #for _ in range(iterations):
    while True:
        randNode = getRandomNode(mapData, possibleVelocity)
        
        nearestNode = getNearestNode(nodes, randNode)
        
        newNode = getNewNode(nearestNode, randNode, stepSize, scaler)
        
        # Check if newNode is valid and obstacle-free
        if newNode and isNewNodeObstacleFree(newNode, nearestNode, mapData,  binaryImage):

            nearNodes = getNearNodes(nodes, newNode, stepSize,binaryImage)
            if not nearNodes:
                selectNewParentNode(nearestNode, newNode, nearNodes)
                rewireNearNodes(nearNodes, newNode)
                
                nodes.append(newNode)
                hit = hit+1
                #plot_tree(nodes, newNode, mapData, goal)  # 현재 트리를 플롯
                    #if newNode and isGoalReached(newNode, goal, threshold):
                    #plot_tree(nodes, newNode, mapData, goal)  # 현재 트리를 플롯
                    #print("total E = ", int(getTotalPower(start,newNode,goal)),"W")
                    #print("total T = ", int(newNode.cost),"sec")
                    #print("E / T = ",int(getTotalPower(start,newNode,goal) / newNode.cost), "W/s")
                print(hit)

                if hit == 1000:
                    #plot_tree(nodes, newNode, mapData, goal)  # 현재 트리를 플롯
                    #print("total E = ", int(getTotalPower(start,newNode,goal)),"W")
                    #print("total T = ", int(newNode.cost),"sec")
                    #print("E / T = ",int(getTotalPower(start,newNode,goal) / newNode.cost), "W/s")
                    return nodes, hit
            
            

    # Check if the goal is reached
            #if newNode and isGoalReached(newNode, goal, threshold):
                #print("Goal reached!")
                #plot_tree(nodes, newNode, mapData, goal)  # 현재 트리를 플롯
                
                #print("total E = ", int(getTotalPower(start,newNode,goal)),"W")
                #print("total T = ", int(newNode.cost),"sec")
                #print("E / T = ",int(getTotalPower(start,newNode,goal) / newNode.cost), "W/s")
                #return nodes
    
      


    return nodes, hit


    
