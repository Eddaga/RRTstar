from RRTstar import *
import signal

def handler(signum, frame):
    
    print("quit making Tree?") 
    exit()


def main():
    start = Node(850, 1000, 1)
    goal = Node(150, 1000, 0)
    iterations = 1000
    stepSize = 2 # 0.277777hour = 10sec
    mapMaxSize = [1000, 2000]
    possibleVelocity = 42# 150.0 km/h * 100 / 3600 = 41.16667m/s
    # tree = treeLoader()
    tree = []
    


    signal.signal(signal.SIGINT, handler)
    rrtStar(tree, start, goal, iterations, stepSize, mapMaxSize, possibleVelocity)


if __name__ == "__main__":
    main()