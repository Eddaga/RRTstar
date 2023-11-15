import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import sys
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt

from sklearn.datasets import load_wine
from sklearn.metrics import accuracy_score

# Define hyperparameters
PATH = "need to rewrite code for model load.!!"

rowtoskip = 2500
hidden_size = 10
output_size = 1
num_epochs = 2500
batch_size = 7000
learning_rate = 0.1
outlierClear = 0
makeModel = 1
saveModel = 1

if len(sys.argv) != 2:
    print("write file name please\r\n")
    exit()


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if device == 'cpu':
    exit()
else :
    print("cuda working\r\n")
# Data NameTag
#       A
#       tick
#       B       C       D   
#       break   accel   pittot
#       E       F
#       bTemp   bPress
#       G       H       I       J       K       L
#       aAngle  aC      aTemp   aTq     aVel    aV
#       M       N       O       P       Q       R
#       bAngle  bC      bTemp   bTq     bVel    bV
#       S       T       U       V
#       fTemp   fC      fSOC    fV
#       W       X       Y       Z
#       bTemp   bC      bSOC    bV
#       AA      AB      AC      AD
#       tTemp   tC      tSOC    tV
#       AE      AF
#       latti  longi
#       AG      AH      AI      AJ      AK      AL      AM
#       AccX    AccY    AccZ    GyroX   GyroY   GyroZ   Temp
#       AN      AO      AP
#       Sec     Min     Hour
#       AQ      AR      AS      AT
#       Roll    Pitch   Yaw     Handle(Vehicle tilt)
#       

print("C,Q,AT")
data = pd.read_excel(datapathToRead, header=None, usecols="C,Q,AT", skiprows=rowtoskip)
input_size = 3

# Normalize data
input_scaler = MinMaxScaler()
train_data = input_scaler.fit_transform(train_data)

# Define the neural network
class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


# Move data to device
train_data = torch.tensor(train_data, dtype=torch.float32).to(device)

# Train the model

model = MLP(input_size, hidden_size, output_size).to(device)
model.load_state_dict(torch.load(datapathToWriteModel))
model.eval()

#get P
with torch.no_grad():
        # Compute validation loss
    val_outputs = model(val_data)
