import numpy as np
import joblib
import torch
from getLastCandle import fetchData
from LoadModel import loadModel, Model
from saveRes import savePred
from BitmexPrice import Get15mInd, Get1hInd, Get2hInd, Get4hInd


def trade(timeframe):

    if timeframe == "15_min":
        cpT, rsiT, momT, maT = Get15mInd()
    if timeframe == "1_h":
        cpT, rsiT, momT, maT = Get1hInd()
    if timeframe == "2_h":
        cpT, rsiT, momT, maT = Get2hInd()
    if timeframe == "4_h":
        cpT, rsiT, momT, maT = Get4hInd()

    scalerCp = joblib.load("../saved_model/scaler/" + timeframe + "/scaler_cp.pkl")
    scalerRsi = joblib.load("../saved_model/scaler/" + timeframe + "/scaler_rsi.pkl")
    scalerMom = joblib.load(
        "../saved_model/scaler/" + timeframe + "/scaler_momentum.pkl"
    )

    cp = np.array(cpT).reshape(1, np.array(cpT).shape[0])
    rsi = np.array(rsiT).reshape(1, np.array(rsiT).shape[0])
    momentum = np.array(momT).reshape(1, np.array(momT).shape[0])
    scaledMa = np.array(maT).reshape(1, np.array(maT).shape[0])

    scaledCp = scalerCp.transform(cp)
    scaledRsi = scalerRsi.transform(rsi)
    scaledMom = scalerMom.transform(momentum)

    X = torch.Tensor(np.concatenate((scaledCp, scaledRsi, scaledMom, scaledMa), 1))

    for delay in range(1, 17):
        model = loadModel(timeframe, delay).eval()

        out = model(X)
        state: str = "0" if out[0][0] > out[0][1] else "1"
        proba = format(out.detach()[0][int(state)].item(), ".3f")

        savePred(delay, state, proba, timeframe)


# TODO now we let some recording, and after work on getting the accuracy of each prediction
