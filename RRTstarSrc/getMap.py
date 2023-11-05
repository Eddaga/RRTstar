from PIL import Image
import numpy as np

    
def getMapData(path,realDistance):
    # 1. load image
    original_image = Image.open(path)
    
    # 2. change image to binary scale
    threshold = 100  # 
    binary_image = original_image.convert('L').point(lambda p: p < threshold and 1)

    # 2. create image scaler // total Image Pixel / Real distance(m) -> x pixel/m => x pixel per 1m.

    binaryNP = np.array(binary_image)
    rows, cols = binaryNP.shape    # it returns total size of image.

    imagePixel = rows
    #realDistance = 1200 # it means 1200m
    domain = 10 # grid scalse as 10m.
    scaler = imagePixel / realDistance * domain

    # 3. make black list 
    blackList = []
    whiteList = []
    
    for i in range(0, imagePixel, int(scaler)):
        for j in range(0 , imagePixel, int(scaler)):
            if binaryNP[i, j] == 0:  # 검은 픽셀 - 트랙
                #print(i,j)
                blackList.append((i, j))
            else:  # 흰 픽셀 - 장애물
                whiteList.append((i, j))
    mapData = [blackList, whiteList]
    
    return mapData, scaler