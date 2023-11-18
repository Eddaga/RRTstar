from RRTutils import *
import math
from MLP import *
import numpy as np



# import MLP~~

def getOptimalPath(startNode, newNode):
    optimalPath = []
    current = newNode
    while current.parent is not None:  # Continue until you reach the start node (which has no parent)
        optimalPath.insert(0,current)
        current = current.parent
    optimalPath.insert(0,startNode)
    return optimalPath 

def getMlpParams(childNode, parentNode):
    velocity = ((childNode.velocity + parentNode.velocity) / 2)
    accelPress = velocity / getTimeSteer(childNode, parentNode)

    # vehicle's tilt is opposite of theta, so add 90 maybe..?
    childDegree = math.degrees(math.atan2( parentNode.y - childNode.y, parentNode.x - childNode.x))
    if parentNode.parent is not None:
        parentDegree = math.degrees(math.atan2( parentNode.parent.y - parentNode.y, parentNode.parent.x - parentNode.x))
    else:
        parentDegree = 0
    tilt = childDegree - parentDegree
    return accelPress, velocity, tilt


def getTotalPower(startNode, newNode, goalNode):
    optimalPath = getOptimalPath(startNode,newNode)
    current = newNode
    #optimalPath = optimalPath.append(goalNode)
    #goalNode.parent = newNode
    #current = goalNode
    inputData = []
    T = []
    E = 0
    totalT = 0
    j = 0

    while current.parent is not None:
        accelPress, velocity, tilt = getMlpParams(current, current.parent)
        inputData.append([accelPress, velocity, tilt])
        T.append(getTimeSteer(current,current.parent))
                
        current = current.parent
        j = j+1
    
    P = energyCalculator(inputData)
    P = P.flatten().tolist()
    print("s")
    
    print(len(P))
    print(j)
    print("s")
    
    optimalPath.reverse()
    current = newNode
    Ti = 0

    for i in range(len(P)):
        

        #print("cost = ",optimalPath[i].cost - optimalPath[i].cost ,optimalPath[i].x, optimalPath[i].y)
        print("OPT cost = ",optimalPath[i].cost - optimalPath[i].parent.cost, optimalPath[i].x, optimalPath[i].y)

        print("CUT cost = ",getTimeSteer(current, current.parent),current.x, current.y)
        print("")
        current = current.parent

        E = E + P[i] * T[i]
        totalT = totalT + T[i]



        


    
    exit()
    return E