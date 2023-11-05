from RRTsubfunc import *
import matplotlib.pyplot as plt



        
def plot_map(map_data, scaler):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    
    black_list, white_list = map_data
    
    # Assuming that the map data is normalized to a grid where each cell represents 'domain' meters
    for coord in black_list:
        rect = plt.Rectangle((coord[1]/scaler, coord[0]/scaler), 1, 1, color='black')
        ax.add_patch(rect)

    plt.xlim(0, int(np.ceil(len(map_data[1])/scaler)))
    plt.ylim(0, int(np.ceil(len(map_data[1])/scaler)))
    plt.xlabel('meters')
    plt.ylabel('meters')
    plt.grid(True)


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


    
