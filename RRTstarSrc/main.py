
from getMap import *
from RRT import *
import sys
import select

def get_input_with_timeout(prompt, timeout):
    print(prompt, end='', flush=True)
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()
    return None


def plot_map(mapData, scaler):

    # 흑색 픽셀과 백색 픽셀의 위치 목록을 얻습니다.
    blackList, whiteList = mapData
    print(len(blackList))
    print("hello")
    i = 0
    # 흑색 픽셀을 그립니다.
    for point in blackList:
        i = i+1
        print(i)
        plt.scatter(point[1], point[0], c='black')
    
    # 백색 픽셀을 그립니다. (필요한 경우)
    for point in whiteList:
        i = i+1
        print(i)
        plt.scatter(point[1], point[0], c='white')

    plt.gca().invert_yaxis()  # y축을 이미지와 동일한 방향으로 뒤집습니다.
    plt.show()  # 그래프를 표시합니다.




def main():
    start = Node(850, 1000, 1)
    goal = Node(150, 1000, 0)
    iterations = 1000
    stepSize = 2 # 0.277777hour = 10sec
    mapMaxSize = [1000, 2000]
    possibleVelocity = 42# 150.0 km/h * 100 / 3600 = 41.16667m/s
    threshold = 6
    mapPath = "../mapImage/9track.png"
    realDistance = 1200
    # tree = treeLoader()

    

    print("RRTstar Algorithm Start. Please Load MapData Please")
    mapData, scaler = getMapData(mapPath,realDistance)
     
    
    #plt.ion()  # 인터랙티브 플로팅 시작
    plot_map(mapData, scaler)
    

        
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
        print("1 set iteration end. you want to do make it again?")
        user_input = get_input_with_timeout("If you wan to stop, enter something within 1 seconds: ", 1)
        if user_input:
            print(f"You entered: {user_input}")
            break
        else:
            tree = rrtStar(tree, iterations, stepSize, mapMaxSize, possibleVelocity, mapData, scaler, goal, threshold)

    plt.ioff()  # 모든 것이 끝나면 인터랙티브 플로팅을 끕니다
    plt.show()  # 최종 플롯을 표시합니다


if __name__ == "__main__":
    

    main()

    