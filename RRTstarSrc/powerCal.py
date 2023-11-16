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
    parentDegree = math.degrees(math.atan2( parentNode.parent.y - parentNode.y, parentNode.parent.x - parentNode.x))
    tilt = childDegree - parentDegree
    return accelPress, velocity, tilt


def getTotalPower(startNode, newNode, goalNode):
    optimalPath = getOptimalPath(startNode,newNode)
    current = newNode
    #optimalPath = optimalPath.append(goalNode)
    #goalNode.parent = newNode
    #current = goalNode
    inputData = []

    while current.parent.parent is not None:
        accelPress, velocity, tilt = getMlpParams(current, current.parent)
        inputData.append([accelPress, velocity, tilt])
        current = current.parent
    
    E = energyCalculator(inputData)
    return E

