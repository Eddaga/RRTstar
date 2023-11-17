import torch
import torch.nn as nn
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt

from sklearn.datasets import load_wine
from sklearn.metrics import accuracy_score

def deviceCheck():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if device == 'cpu':
        exit()
    else :
        print("cuda working\r\n")

    return device

def energyCalculator(inputData):
    
    modelPath = "/home/esl/kyuyong/erclAllInOne/data/date/01091158/MLP/MLPmodel/01091158model.pt"
    device = deviceCheck()

    # Define hyperparameters
    hidden_size = 10
    output_size = 1
    input_size = 3

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

    input_scaler = MinMaxScaler()
    inputData = input_scaler.fit_transform(inputData)

    # Move data to device
    inputData = torch.tensor(inputData, dtype=torch.float32).to(device)

    # Train the model

    model = MLP(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(torch.load(modelPath))
    model.eval()

    #get P
    with torch.no_grad():
        E = model(inputData)

    return E.cpu().detach().numpy()

