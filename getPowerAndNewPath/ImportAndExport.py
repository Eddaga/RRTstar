import pandas as pd

def loadPath(hitNum):
    filePath = "../foundPath" + str(hitNum) + "pathNodes.xlsx"
    data = pd.read_excel(filePath)
    return data