
def computeRSI(last_cp):

    firstRSI = 0.0
    avgGain = 0.0
    avgLoss = 0.0

    differenceCP = [0] * (len(last_cp) - 1)
    rsi = [0] * (len(differenceCP) - 13)

    for i in range(len(last_cp) - 1):
        differenceCP[i] = last_cp[i + 1] - last_cp[i]

    for j in range(0, 14):
        avgGain += max(differenceCP[j], 0)
        avgLoss -= min(differenceCP[j], 0)

    avgGain /= 14
    avgLoss /= 14
    rsi[0] = 100 - 100 / (1 + avgGain / avgLoss)

    for i in range(14, len(differenceCP)):
        avgGain = (avgGain * 13 + max(differenceCP[i], 0))/14
        avgLoss = (avgLoss * 13 - min(differenceCP[i], 0)) / 14
        rsi[i - 13] = 100 - 100 / (1 + avgGain / avgLoss)

    # rsi[0] is the last rsi (the one of last full candle)
    print(rsi)
