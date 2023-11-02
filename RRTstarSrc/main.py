
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

def plot_tree(nodes, newNode, goal):
    # plt.clf()  # 현재 피규어를 클리어하지 마세요
    for node in nodes:
        if node.parent is not None:
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], 'b-')
    plt.plot(newNode.x, newNode.y, 'go', label='새 노드')  # 새 노드는 녹색 점으로 표시
    plt.pause(0.01)  # 플롯을 업데이트 하기 위해 잠시 멈춤
    
def main():
    start = Node(850, 1000, 1)
    goal = Node(150, 1000, 0)
    iterations = 1000
    stepSize = 2 # 0.277777hour = 10sec
    mapMaxSize = [1000, 2000]
    possibleVelocity = 42# 150.0 km/h * 100 / 3600 = 41.16667m/s
    threshold = 6
    mapPath = "../MAP.jpg"
    # tree = treeLoader()

    plt.ion()  # 인터랙티브 플로팅 시작

    print("RRTstar Algorithm Start. Please Load MapData Please")
    mapData, scaler = getMapData(mapPath)

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

    