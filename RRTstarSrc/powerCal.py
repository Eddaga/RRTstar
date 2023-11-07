import RRTutils
# import MLP~~
def mlpParameters(node1,node2):
    velocity = (node1.velocity + node2.velocity) / 2
    # deal accelPress as torqueMode.. so accelPress = accelration
    accelPress = (node1.cost - node2.cost) # get accel equation
    tilt = (node1.x - node2.y) # kind of this function to get tilts

    return accelPress, velocity, tilt



'''
def asklbval(import powermodels(MLP~~~)

    return P~~
'''