import time
import sched
import schedule
from openTrade import trade


def p15m():
    print("making a 15m prediction")
    trade("15_min")
    return


def p1h():
    print("making a 1 hour prediction")
    trade("1_h")
    return


def p2h():
    print("making a 2 hour prediction")
    trade("2_h")
    return


def p4h():
    print("making a 4 hour prediction")
    trade("4_h")
    return


schedule.every(15).minutes.at(":03").do(p15m)
schedule.every(1).hour.at("02:00").do(p1h)
schedule.every(2).hours.at("04:00").do(p2h)
schedule.every(4).hours.at("08:00").do(p4h)

while True:
    schedule.run_pending()
    time.sleep(1)
