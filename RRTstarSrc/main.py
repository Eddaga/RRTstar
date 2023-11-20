
from getMap import *
from RRT import *
import sys
import select
import pandas as pd


def main():
    start = Node(880, 630, 1 )
    goal = Node(880,550, 0)
    stepSize = 2.3#0.5
    mapMaxSize = [1200, 1200]
    possibleVelocity = 41# 150.0 km/h * 100 / 3600 = 41.16667m/s
    threshold = 50 #for isGoalReached(euclidian distance)
    mapPath = "../mapImage/9track2.png"
    realDistance = 1200
    # tree = treeLoader()

    

    print("RRTstar Algorithm Start. Please Load MapData Please")
    binaryImage, mapData, scaler = getMapData(mapPath,realDistance)
     
    
    plt.ion()  # 인터랙티브 플로팅 시작
    plt.xlim([0, 1200])
    plt.ylim([0, 1200])
  
    #plotMap(mapData)
    
    
    hit = 0
    totalHit = 0        
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

    tree, hit = rrtStar(tree, start,  stepSize,  possibleVelocity, mapData, scaler, goal, threshold,binaryImage)
    totalHit = totalHit + hit
    save_to_excel(tree,mapData,scaler,totalHit)
    print(totalHit)
    i = 1
    while True:
        #user_input = get_input_with_timeout("1 set iteration end. If you wan to stop, enter something within 1 seconds: ", 0.1)
        #if user_input:
        #    print(f"You entered: {user_input}")
        #    break
        #else:
        tree, hit = rrtStar(tree, start,  stepSize,  possibleVelocity, mapData, scaler, goal, threshold,binaryImage)
        totalHit = totalHit + hit
        print(totalHit)

        if totalHit == 5000:
            save_to_excel(tree,mapData,scaler,totalHit)
        if totalHit == 10000*i:
            save_to_excel(tree,mapData,scaler,totalHit)
            i = i+1
        
    
def get_input_with_timeout(prompt, timeout):
    print(prompt,flush=True)
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()
    return None


def plotMap(mapData):

    # 흑색 픽셀과 백색 픽셀의 위치 목록을 얻습니다.
    blackList, whiteList = mapData
    #print(len(blackList))
    # 흑색 픽셀을 그립니다.
    xCoords = []
    yCoords = []

    # Loop through each point in the blackList
    for point in whiteList:
  

        x = point[0]
        xCoords.append(x)  
        
        y = point[1]
        yCoords.append(y) 

    # Plot all points at once
    plt.scatter(xCoords, yCoords, c='black', s=1)  # s is the size of the point
    plt.pause(0.01)
    # Show the plot   



if __name__ == "__main__":
    

    main()

    