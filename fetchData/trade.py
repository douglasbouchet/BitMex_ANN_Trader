import numpy as np
import joblib
import torch
from getLastCandle import fetchData
from LoadModel import loadModel, Model

timeframe = "15m"

scalerCp = joblib.load('../saved_model/scaler/scaler_cp.pkl')
scalerRsi = joblib.load('../saved_model/scaler/scaler_rsi.pkl')
scalerMom = joblib.load('../saved_model/scaler/scaler_momentum.pkl')

cpT, rsiT, momentumT, maT = fetchData(timeframe)

cp = np.array(cpT).reshape(1, np.array(cpT).shape[0])
rsi = np.array(rsiT).reshape(1, np.array(rsiT).shape[0])
momentum = np.array(momentumT).reshape(1, np.array(momentumT).shape[0])
scaledMa = np.array(maT).reshape(1, np.array(maT).shape[0])

scaledCp = scalerCp.transform(cp)
scaledRsi = scalerRsi.transform(rsi)
scaledMom = scalerMom.transform(momentum)

X = torch.Tensor(np.concatenate((scaledCp, scaledRsi, scaledMom, scaledMa), 1))

model = loadModel("15_min", 1)

out = model(X)

print(out)
