import pandas as pd
import numpy as np

def loadPathData(fileName):
    # Load the Excel file
    data = pd.read_excel(fileName)

    # Ensure the correct columns are present
    expected_columns = ['X', 'Y', 'Velocity', 'Cost']
    if not all(column in data.columns for column in expected_columns):
        raise ValueError(f"Excel file must contain columns: {expected_columns}")

    return data

def getAccelerations(data):
    # Calculate differences in velocity and time
    velocity_diff = data['Velocity'].diff()
    time_diff = data['Cost'].diff()

    # Calculate accelerations
    accelerations = velocity_diff / time_diff
    accelerations = np.nan_to_num(accelerations, nan=0.0)
    return accelerations

def getPedalIntensity(acceleration):
    pedal_intensities = np.abs(acceleration) / 5
    pedal_intensities = np.clip(pedal_intensities, 0, 1)  # Clipping between 0 and 1

    return pedal_intensities

def removeRowsAfterCostDecreases(data):
    # Find the first index where 'Cost' decreases
    decreaseIndex = (data['Cost'].diff() < 0).idxmax()

    # Check if there is an actual decrease or the maximum cost is at the end
    if decreaseIndex == 0 or decreaseIndex == len(data) - 1:
        return data  # No change if cost never decreases or decreases only at the last row

    # Remove rows from the decrease point
    return data[:decreaseIndex]



def calculateAngle(data):
    # Initialize angles with zeros
    angles = np.zeros(len(data))

    # Calculate angles for each node
    for i in range(1, len(data)):
        dx = data['X'].iloc[i] - data['X'].iloc[i-1]
        dy = data['Y'].iloc[i] - data['Y'].iloc[i-1]
        angles[i] = np.degrees(np.arctan2(dy, dx))

    # Calculate angle changes
    angle_changes = np.diff(angles, prepend=angles[0])

    # Add angles and angle changes to the DataFrame
    
    data['AngleChange'] = angle_changes

    return data['AngleChange']


def saveNodesPower(powers,fileName):
    df = pd.DataFrame(powers, columns=['Power'])
    df.to_excel(fileName, index=False)
    
def calculateCost(T):
    """
    Calculate the cost for each element in T.
    The cost for each element is defined as the sum of the current and the previous element.
    For the first element, the cost is just the value of the element itself.
    """
    costs = []
    cumulative_sum = 0
    for value in T:
        cumulative_sum += value
        costs.append(cumulative_sum)
    return costs


def saveUpdatedNodesPowerAndVelocityCost(powers,velocities,times,cost,fileName):
    df = pd.DataFrame({
                        'Power' : powers,
                        'Velocity' : velocities,
                        'Time': times,
                        'Cost': cost})
    df.to_excel(fileName, index=False)

