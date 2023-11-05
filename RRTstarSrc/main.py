
from getMap import *
from RRT import *
import sys
import select

def get_input_with_timeout(prompt, timeout):
    print(prompt,flush=True)
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()
    return None


def plotMap(mapData, scaler):

    # 흑색 픽셀과 백색 픽셀의 위치 목록을 얻습니다.
    blackList, whiteList = mapData
    print(len(blackList))
    i = 1
    j = 1
    # 흑색 픽셀을 그립니다.
    xCoords = []
    yCoords = []

    # Loop through each point in the blackList
    for point in blackList:
        if i == 100:
            i = 1
            j = j+1
            print(j*100,"/",len(blackList))
        i = i+1    

        x = point[1]
        xCoords.append(x)  
        
        y = point[0]
        yCoords.append(y) 

    # Plot all points at once
    plt.scatter(xCoords, yCoords, c='black', s=1)  # s is the size of the point
    plt.pause(0.01)
    # Show the plot
    




def main():
    start = Node(930, 570, 1)
    goal = Node(930, 610, 0)
    iterations = 1000
    stepSize = 2 # 0.277777hour = 10sec
    mapMaxSize = [1000, 2000]
    possibleVelocity = 42# 150.0 km/h * 100 / 3600 = 41.16667m/s
    threshold = 6
    mapPath = "../mapImage/9track2.png"
    realDistance = 1200
    # tree = treeLoader()

    

    print("RRTstar Algorithm Start. Please Load MapData Please")
    mapData, scaler = getMapData(mapPath,realDistance)
     
    
    plt.ion()  # 인터랙티브 플로팅 시작
    plt.xlim([0, 1200])
    plt.ylim([0, 1200])
  
    plotMap(mapData, scaler)
    
    

        
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

    tree = rrtStar(tree, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, goal, threshold)

    while True:
        user_input = get_input_with_timeout("1 set iteration end. If you wan to stop, enter something within 1 seconds: ", 0.1)
        if user_input:
            print(f"You entered: {user_input}")
            break
        else:
            tree = rrtStar(tree, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, goal, threshold)
    print("hello!")
    plt.ioff()  # 모든 것이 끝나면 인터랙티브 플로팅을 끕니다

    plt.show()  # 최종 플롯을 표시합니다



if __name__ == "__main__":
    

    main()

    