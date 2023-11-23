from PIL import Image

def getMapData(path, realDistance):
    # 1. 이미지 로드
    original_image = Image.open(path)
    
    # 2. 이진 스케일로 이미지 변환
    threshold = 1
    binaryImage = original_image.convert('L').point(lambda p: p < threshold and 1)

    # 이미지 크기 반환
    width, height = binaryImage.size

    imagePixel = height
    domain = 10  # 그리드 스케일 10m 단위
    scaler = imagePixel / realDistance * domain

    # 3. 흑백 리스트 생성
    blackList = []
    whiteList = []
    
    # blackList 생성 (10단위 증가)
    for i in range(0, width, int(scaler)):
        for j in range(0, height, int(scaler)):
            pixel_value = binaryImage.getpixel((i, j))
            if pixel_value == 1:  # 검은 픽셀 - 트랙
                blackList.append((i, j))

    # whiteList 생성 (모든 픽셀 검사)
    for i in range(0, width, int(scaler)):
        for j in range(0, height, int(scaler)):
            pixel_value = binaryImage.getpixel((i, j))
            if pixel_value != 1:  # 흰 픽셀 - 장애물
                whiteList.append((i, j))

    mapData = [blackList, whiteList]
    
    return binaryImage, mapData, scaler