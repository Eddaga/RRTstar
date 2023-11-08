import RRTutils
# import MLP~~

def getOptimalPath(startNode, newNode):
    optimalPath = []
    current = newNode
    while current.parent is not None:  # Continue until you reach the start node (which has no parent)
        optimalPath.insert(0,current)
        current = current.parent
    optimalPath.insert(0,startNode)
    print(optimalPath[0].x," ",optimalPath[1].y)
    return optimalPath 

def getTotalPower(startNode,goalNode):
    optimalPath = getOptimalPath(startNode,goalNode)
    

    return Energy
    

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