import datetime
from datetime import timedelta
import csv
import os.path


def savePred(delay, state, proba, timeframe):
    switcher = {
        "15_min": timedelta(minutes=15 * delay),
        "1_h": timedelta(hours=delay),
        "2_h": timedelta(hours=2 * delay),
        "4_h": timedelta(hours=4 * delay),
    }

    cur = datetime.datetime.now()

    switcher2 = {
        "15_min": datetime.datetime(
            cur.year, cur.month, cur.day, cur.hour, (cur.minute // 15 * 15) - 15, 0
        ),
        "1_h": datetime.datetime(cur.year, cur.month, cur.day, cur.hour - 1, 0, 0),
        "2_h": datetime.datetime(
            cur.year, cur.month, cur.day, cur.hour // 2 * 2 - 2, 0, 0
        ),
        "4_h": datetime.datetime(
            cur.year, cur.month, cur.day, cur.hour // 4 * 4 - 4, 0, 0
        ),
    }

    current = switcher2.get(timeframe)
    next = current + switcher.get(timeframe)

    if not os.path.isfile(
        "/Users/douglasbouchet/HXRO_ANN_Trader/prediction/"
        + timeframe
        + "/trade_"
        + str(delay)
        + ".csv"
    ):
        with open(
            "/Users/douglasbouchet/HXRO_ANN_Trader/prediction/"
            + timeframe
            + "/trade_"
            + str(delay)
            + ".csv",
            "w",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow(["open ts", "delay", "state", "proba", "close ts"])
            writer.writerow([current, delay, state, str(proba), next])
    else:
        with open(
            "/Users/douglasbouchet/HXRO_ANN_Trader/prediction/"
            + timeframe
            + "/trade_"
            + str(delay)
            + ".csv",
            "a",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow([current, delay, state, str(proba), next])
