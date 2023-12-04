from GPANP import *
from MLP import *


pd.set_option('mode.chained_assignment',  None) # <==== 경고를 끈다

def main():
    fileName = "/home/esl/kyuyong/RRTstar/foundPath/50000pathNodes.xlsx"
    fileSavePath1 = "/home/esl/kyuyong/RRTstar/Power/Full50000.xlsx"
    fileSavePath2 = "/home/esl/kyuyong/RRTstar/Power/Cut50000.xlsx"
    expectedPower = 5000000
    coefficients = [0.7074,0.0324,0.0580]



    # 1. load Path Data
    data = removeRowsAfterCostDecreases(loadPathData(fileName))
    T = np.diff(data['Cost'])
    T = np.insert(T,0,0)
    # 2. make MLP data from Path data
    accelerations = getAccelerations(data)
    
    
    velocity = data['Velocity']
    angle = calculateAngle(data)
    pedalIntensities = getPedalIntensity(velocity,accelerations,coefficients)
    dataForMLP = normalizerForDataForMLP(pedalIntensities,velocity,angle)
    
    # 3. calculate Power for Each Node and Save
    P = energyCalculator(dataForMLP).flatten()
    saveNodesPower(P,fileSavePath1)

    
    # 4. get total E!

    E = sum(P * T)

    print(E)

    # 5. if Power is Larger than we expected, minus 1 node's velocity
    while True:
        

        velocityAdjusted = False
        for i in range(len(data) - 1, -1, -1):
            if data['Velocity'].iloc[i] > 2:
                data['Velocity'].iloc[i]  = data['Velocity'].iloc[i] - 1  # 속도 감소
                velocityAdjusted = True

                # Recalculate power and energy from this node to the end
                for j in range(i, len(data) - 1):
                    distance = np.sqrt((data['X'].iloc[j + 1] - data['X'].iloc[j])**2 + (data['Y'].iloc[j + 1] - data['Y'].iloc[j])**2)
                    avg_velocity = (data['Velocity'].iloc[j] + data['Velocity'].iloc[j + 1]) / 2
                    T[j + 1] = distance / avg_velocity
                
                dataForMLP = normalizerForDataForMLP(getPedalIntensity(data['Velocity'], getAccelerations(data),coefficients), data['Velocity'], calculateAngle(data))
                #dataForMLP = list(zip(getPedalIntensity(data['Velocity'], getAccelerations(data),coefficients), data['Velocity'], calculateAngle(data)))
                #dataForMLP = list(zip(pedalIntensities, data['Velocity'], calculateAngle(data)))

                dataForMLP[0] = (0,1.0,0)
                P = energyCalculator(dataForMLP).flatten()
                E = sum(P * T)
                print(E)
                if E <= expectedPower:
                    saveUpdatedNodesPowerAndVelocityCost(P,data['Velocity'],T, calculateCost(T),fileSavePath2)
 
                    return
        

        if not velocityAdjusted:
            print("Unable to reduce power to expected level")
            
            print(getPedalIntensity(data['Velocity'], getAccelerations(data),coefficients))
            break  # 모든 노드의 속도가 2 이하이면 반복을 중단합니다.
    
    

if __name__ == "__main__":
    main()



    