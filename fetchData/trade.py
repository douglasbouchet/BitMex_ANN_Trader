import numpy as np
import joblib
import torch
from getLastCandle import fetchData
from LoadModel import loadModel, Model
from saveRes import savePred
from BitmexPrice import Get15mInd, Get1hInd, Get2hInd, Get4hInd


def trade(timeframe):
    switcher = {
        "15_min": Get15mInd(),
        "1_h": Get1hInd(),
        "2_h": Get2hInd(),
        "4_h": Get4hInd(),
    }
    return switcher.get(timeframe)


timeframe = "2_h"
delay = 5

cpT, rsiT, momT, maT = trade(timeframe)

scalerCp = joblib.load('../saved_model/scaler/' +
                       timeframe + '/scaler_cp.pkl')
scalerRsi = joblib.load('../saved_model/scaler/' +
                        timeframe + '/scaler_rsi.pkl')
scalerMom = joblib.load('../saved_model/scaler/' +
                        timeframe + '/scaler_momentum.pkl')

cp = np.array(cpT).reshape(1, np.array(cpT).shape[0])
rsi = np.array(rsiT).reshape(1, np.array(rsiT).shape[0])
momentum = np.array(momT).reshape(1, np.array(momT).shape[0])
scaledMa = np.array(maT).reshape(1, np.array(maT).shape[0])

scaledCp = scalerCp.transform(cp)
scaledRsi = scalerRsi.transform(rsi)
scaledMom = scalerMom.transform(momentum)

X = torch.Tensor(np.concatenate((scaledCp, scaledRsi, scaledMom, scaledMa), 1))

model = loadModel(timeframe, delay).eval()

out = model(X)

savePred(delay, out.detach().numpy())

# TODO each 15 minutes, make a new prediction for delay 1,2,3, store the prediction (with the timestamp for example)
# TODO see how we can get the result of each moon/rekt, and save them with a timestamp and the result
# make recording during for example 10 hours -> 40 trades, and see the prediction
