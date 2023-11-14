import RRTutils
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
    accelPress = ((childNode.velocity + parendNode.velocity) / 2) / childNode.cost 

    return accelPress, Velocity, tilt


def getTotalPower(startNode, newNode, goalNode):
    optimalPath = getOptimalPath(startNode,newNode)
    optimalPath = optimalPath.append(goalNode)
    goalNode.parent = newNode
    current = goalNode

    while current.parent is not None:
        getMlpParams
        

    
    

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