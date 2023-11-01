from RRTstar import *
from getMap import *

def main():
    start = Node(850, 1000, 1)
    goal = Node(150, 1000, 0)
    iterations = 1000
    stepSize = 2 # 0.277777hour = 10sec
    mapMaxSize = [1000, 2000]
    possibleVelocity = 42# 150.0 km/h * 100 / 3600 = 41.16667m/s
    threshold = 6
    # tree = treeLoader()
    
    print("RRTstar Algorithm Start. Please Load MapData Please")
    mapData, scaler = getMapData(path)

    print("Load Exist Tree or Make New Tree?")
    while 1:

        print("Load = 0, New = 1")
        a = int(input("method :: "))
        if a == 0:
            print("load exist tree data")
            #tree = loadTree()
            break

        elif a == 1:
            print("make new tree")
            tree = [start]
            break

        else:
            print("enter correct num please.")
 
    tree = rrtStar(tree, goal, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler)

    # Check if the goal is reached
    if isGoalReached(newNode, goal, threshold):
        print("Goal reached!")
        return nodes, newNode  # or you might return a path, depending on your use case
        
    print("Goal not reached within the specified iterations.")
    return nodes, False  # or you might return None or an empty path, depending on your use case     


if __name__ == "__main__":
    main()