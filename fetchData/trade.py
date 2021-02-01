import numpy as np
import joblib
import torch
from getLastCandle import fetchData
from LoadModel import loadModel, Model
from saveRes import savePred

timeframe = "15m"
time_frame = "15_min"
delay = 2

scalerCp = joblib.load('../saved_model/scaler/ ' +
                       time_frame + 'scaler_cp.pkl')
scalerRsi = joblib.load('../saved_model/scaler/' +
                        time_frame + 'scaler_rsi.pkl')
scalerMom = joblib.load('../saved_model/scaler/' +
                        time_frame + 'scaler_momentum.pkl')

cpT, rsiT, momentumT, maT = fetchData(timeframe)

cp = np.array(cpT).reshape(1, np.array(cpT).shape[0])
rsi = np.array(rsiT).reshape(1, np.array(rsiT).shape[0])
momentum = np.array(momentumT).reshape(1, np.array(momentumT).shape[0])
scaledMa = np.array(maT).reshape(1, np.array(maT).shape[0])

scaledCp = scalerCp.transform(cp)
scaledRsi = scalerRsi.transform(rsi)
scaledMom = scalerMom.transform(momentum)

X = torch.Tensor(np.concatenate((scaledCp, scaledRsi, scaledMom, scaledMa), 1))

model = loadModel("15_min", delay).eval()

out = model(X)

print(out.detach().numpy())

savePred(delay, out.detach().numpy())

# TODO each 15 minutes, make a new prediction for delay 1,2,3, store the prediction (with the timestamp for example)
# TODO see how we can get the result of each moon/rekt, and save them with a timestamp and the result
# make recording during for example 10 hours -> 40 trades, and see the prediction
