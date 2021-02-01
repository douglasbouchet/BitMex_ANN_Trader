import datetime
from datetime import timedelta
import csv
import os.path


def savePred(delay, pred):
    cur = datetime.datetime.now()
    current = datetime.datetime(
        cur.year, cur.month, cur.day, cur.hour, (cur.minute//15 * 15), 0)

    next = current + timedelta(minutes=15 * (delay + 1), seconds=-1)

    if not os.path.isfile('/Users/douglasbouchet/HXRO_ANN_Trader/prediction/15m/trade_' + str(delay) + '.csv'):
        with open('/Users/douglasbouchet/HXRO_ANN_Trader/prediction/15m/trade_' + str(delay) + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time prediction",
                             "Time realisation", "Long/Short"])
            writer.writerow([current, next, pred[0]])
    else:
        with open('/Users/douglasbouchet/HXRO_ANN_Trader/prediction/15m/trade_' + str(delay) + '.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current, next, pred[0]])
