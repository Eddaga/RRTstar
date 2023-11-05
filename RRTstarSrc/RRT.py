from RRTsubfunc import *
import matplotlib.pyplot as plt



        
def plot_tree(nodes, newNode, goal):
    # plt.clf()  # 현재 피규어를 클리어하지 마세요
    print("helslo")
    for node in nodes:
        if node.parent is not None:
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], 'b-')
    plt.plot(newNode.x, newNode.y, 'go', label='새 노드')  # 새 노드는 녹색 점으로 표시
    plt.pause(10)  # 플롯을 업데이트 하기 위해 잠시 멈춤


def rrtStar(nodes, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, goal, threshold):
    
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
            #plot_tree(nodes, newNode, goal)  # 현재 트리를 플롯
    # Check if the goal is reached
            if newNode and isGoalReached(newNode, goal, threshold):
                print("Goal reached!")
                return nodes
    
      


    return nodes


    
