from RRTsubfunc import *
import matplotlib.pyplot as plt

def plot_map(mapData, scaler):
    # mapData가 장애물의 위치를 포함하고 있다고 가정합니다.
    # 이를 기반으로 지도 위에 장애물을 플롯합니다.
    for obstacle in mapData:
        # 장애물의 크기와 위치를 고려하여 장애물을 플롯
        plt.gca().add_patch(plt.Rectangle((obstacle[0]*scaler, obstacle[1]*scaler), obstacle[2]*scaler, obstacle[3]*scaler, color='red'))

        
def plot_tree(nodes, newNode, goal):
    # plt.clf()  # 현재 피규어를 클리어하지 마세요
    for node in nodes:
        if node.parent is not None:
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], 'b-')
    plt.plot(newNode.x, newNode.y, 'go', label='새 노드')  # 새 노드는 녹색 점으로 표시
    plt.pause(0.01)  # 플롯을 업데이트 하기 위해 잠시 멈춤


def rrtStar(nodes, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, goal, threshold):

    for _ in range(iterations):
        randNode = getRandomNode(mapMaxSize, possibleVelocity)
        nearestNode = getNearestNode(nodes, randNode)
        newNode = getNewNode(nearestNode, randNode, stepSize, scaler)
        
        # Check if newNode is valid and obstacle-free
        if newNode and isNewNodeObstacleFree(newNode, nearestNode, mapData, scaler):
            nearNodes = getNearNodes(nodes, newNode, stepSize)
            selectNewParentNode(nearestNode, newNode, nearNodes)
            rewireNearNodes(nearNodes, newNode)
            nodes.append(newNode)
            plot_tree(nodes, newNode, goal)  # 현재 트리를 플롯
    # Check if the goal is reached
    if isGoalReached(newNode, goal, threshold):
        print("Goal reached!")
        
    else:
        print("Goal not reached within the specified iterations.")
      


    return nodes


    
