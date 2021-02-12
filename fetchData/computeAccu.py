from BitmexPrice import (
    _15m_Candle_All,
    _1h_Candle_All,
    _2h_Candle_All,
    _4h_Candle_All,
    getJson,
)
import datetime
import csv
from datetime import timedelta
import time


def getAll(data, key):
    return [item[1] for item in data if item[0] == key]


tf = ["15_min", "1_h", "2_h", "4_h"]

for timeframe in tf:
    print("wait to compute: " + timeframe)
    print("start: " + timeframe)
    if timeframe == "15_min":
        cp = _15m_Candle_All(getJson())
    if timeframe == "1_h":
        cp = _1h_Candle_All(getJson())
    if timeframe == "2_h":
        cp = _2h_Candle_All(getJson())
    if timeframe == "4_h":
        cp = _4h_Candle_All(getJson())

    time.sleep(30)
    del cp[-1]
    for delay in range(2, 3):
        path = (
            "/Users/douglasbouchet/HXRO_ANN_Trader/prediction/"
            + timeframe
            + "/trade_"
            + str(delay)
            + ".csv"
        )
        goodPred = 0
        badPred = 0
        nb_pred = 0
        with open(path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["open ts"] != "The accuracy is :":
                    nb_pred += 1
                    openTime = row["open ts"]
                    closeTime = row["close ts"]
                    state = row["state"]
                    proba = row["proba"]
                    dO = datetime.datetime.strptime(openTime, "%Y-%m-%d %H:%M:%S")

                    dC = datetime.datetime.strptime(closeTime, "%Y-%m-%d %H:%M:%S")
                    dateO = datetime.datetime(
                        year=dO.year,
                        month=dO.month,
                        day=dO.day,
                        hour=dO.hour,
                        minute=dO.minute,
                        second=dO.second,
                    )
                    dateC = datetime.datetime(
                        year=dC.year,
                        month=dC.month,
                        day=dC.day,
                        hour=dC.hour,
                        minute=dC.minute,
                        second=dC.second,
                    )

                    print(getAll(cp, dateC) != [])
                    if getAll(cp, dateC) != [] and float(proba) > 0.55:
                        openPrice = (getAll(cp, dateO))[0]
                        closePrice = (getAll(cp, dateC))[0]

                        if (state == "0" and closePrice > openPrice) or (
                            state == "1" and closePrice < openPrice
                        ):
                            goodPred += 1
                        else:
                            badPred += 1

        with open(
            path,
            "a",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "The accuracy is :",
                    str(goodPred / (goodPred + badPred) * 100 if badPred != 0 else 100),
                    "Percentage of trades :",
                    str(
                        float(goodPred + badPred) / float(nb_pred) * 100
                        if nb_pred != 0
                        else 0.0
                    ),
                    "",
                ]
            )


# step one,
#  for each timeframe
#       for each delay  open the csv file:
#            iterate over all line:
#               get the open and closing time and state, convert them in good format
#               fetch them in our list, compare the result in function of state
#            add the accuracy at the end of the csv file or anywhere
#
