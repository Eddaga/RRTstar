from RRTsubfunc import *
import matplotlib.pyplot as plt
from main import plotMap
from powerCal import *

        
def plot_tree(nodes, newNode, mapData, goal):
    plt.clf()  # 현재 피규어를 클리어하지 마세요
    plotMap(mapData)
    for node in nodes:
        if node.parent is not None:
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], 'b-', linewidth=0.5)
    plt.plot(newNode.x, newNode.y, 'go', label='새 노드')  # 새 노드는 녹색 점으로 표시

    current = newNode
    while current.parent is not None:  # Continue until you reach the start node (which has no parent)
        plt.plot([current.x, current.parent.x], [current.y, current.parent.y], 'r-', linewidth=1.0)
        current = current.parent  # Move to the next node up the
    print(newNode.cost)
    plt.pause(0.01)  # 플롯을 업데이트 하기 위해 잠시 멈춤


def rrtStar(nodes, start, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, goal, threshold):
    
    for _ in range(iterations):
        randNode = getRandomNode(mapData, possibleVelocity)
        
        nearestNode = getNearestNode(nodes, randNode)
        
        newNode = getNewNode(nearestNode, randNode, stepSize, scaler)
        # Check if newNode is valid and obstacle-free
        if newNode and isNewNodeObstacleFree(newNode, nearestNode, mapData, scaler):
            nearNodes = getNearNodes(nodes, newNode, stepSize)
            selectNewParentNode(nearestNode, newNode, nearNodes)
            rewireNearNodes(nearNodes, newNode)
            nodes.append(newNode)
            #print("hello",newNode.x, newNode.y, newNode.velocity)
            

    # Check if the goal is reached
            if newNode and isGoalReached(newNode, goal, threshold):
                print("Goal reached!")
                #plot_tree(nodes, newNode, mapData, goal)  # 현재 트리를 플롯
                print(" l ")
                print(getTotalPower(start,newNode,goal) * 2, " = E")
                print(" l ")
                return nodes
    
      


    return nodes


    
