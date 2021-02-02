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


timeframe = "4_h"
delay = 3

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
state: str = "0" if out[0][0] > out[0][1] else "1"
proba = format(out.detach()[0][int(state)].item(), '.3f')

savePred(delay, state, proba, timeframe)

# TODO each timeframe: -> 15 min, 1 hour, 2 hour, 4 hour, run this given script:
# each 15 min, script launch 15 min trade,
# each hour, -> script launch 1 hour trade (15 min will also be launch)
# Make a prediction for 1 to 20 delay of the current timeframe

# record the prediction with the following:
# 1: timestamp, 2: delay:, 3: long or short, 4: the timestamp of the objectif (see with delay)
# Close ts represent the time at wich we need to compare the price of the btc


# Then after some hours, we will fetch the new closes prices and open price, compare them
# and compute the accuracy of the predictions.
