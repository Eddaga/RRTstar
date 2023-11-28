from RRTutils import *
import math
from MLP import *
import numpy as np

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


def getTotalPower(optimalPath):
    inputData = []
    T = []
    E = 0
    totalT = 0
    i = 0
    
    for i in range(len(optimalPath)-1):
        accelPress, velocity, tilt = getMlpParams(optimalPath[i+1], optimalPath[i])
        inputData.append([accelPress, velocity, tilt])
        T.append(getTimeSteer(optimalPath[i],optimalPath[i+1]))

    
    P = energyCalculator(inputData)
    P = P.flatten().tolist()
        
    for i in range(len(P)):
        E = E + P[i] * T[i]
        totalT = totalT + T[i]
        
    return E