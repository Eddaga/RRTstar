import pandas as pd
from RRTutils import *

def loadPath(hitNum):
    filePath = "../foundPath/" + str(hitNum) + "pathNodes.xlsx"
    data = pd.read_excel(filePath)
    
    nodes = [Node(row['X'], row['Y'], row['Velocity'], row['Cost']) for index, row in data.iterrows()]
    return nodes