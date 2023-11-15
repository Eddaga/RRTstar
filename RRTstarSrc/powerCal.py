from RRTutils import *
import math
# import MLP~~

def getOptimalPath(startNode, newNode):
    optimalPath = []
    current = newNode
    while current.parent is not None:  # Continue until you reach the start node (which has no parent)
        optimalPath.insert(0,current)
        current = current.parent
    optimalPath.insert(0,startNode)
    return optimalPath 

def getMlpParams(childNode, parentNode, exNodeDegree):
    velocity = ((childNode.velocity + parentNode.velocity) / 2)
    accelPress = velocity / getTimeSteer(childNode, parentNode)

    # vehicle's tilt is opposite of theta, so add 90 maybe..?
    childDegree = degrees(atan2( parentNode.y - childNode.y, parentNode.x - childNode.x))
    parentDegree = degress(atan2( parentNode.parent.y - parentNode.y, parentNode.parent.x - parentNode.x))
    tilt = childDegree - parentDegree
    return accelPress, velocity, tilt


def getTotalPower(startNode, newNode, goalNode):
    optimalPath = getOptimalPath(startNode,newNode)
    current = newNode
    #optimalPath = optimalPath.append(goalNode)
    #goalNode.parent = newNode
    #current = goalNode

    while current.parent is not None:
        accelPress, velocity, tilt = getMlpParams(current, current.parent)
        
        current = current.parent
        

    
    

def mlpParameters(currentNode):
    optimalPath = getOptimalPath(startNode, )
    mlpParamVelocity = (currentNode.velocity + currentNode.parent.velocity) / 2
    # deal accelPress as torqueMode.. so accelPress = accelration
    # get accel equation accel = Velocity / time!
    accelPress = ((currentNode.velocity + currentNode.parent.velocity) / 2) / currentNode.cost - currentNode.parent.cost
    
    tilt = (currentNode.x - currentNode.parent.y) # kind of this function to get tilts

    return accelPress, velocity, tilt



'''
def asklbval(import powermodels(MLP~~~)

    return P~~
'''