import RRTutils
# import MLP~~
def mlpParameters(currentNode):
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