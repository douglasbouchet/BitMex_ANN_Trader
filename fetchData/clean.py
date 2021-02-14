import os
import subprocess


for timeframe in ["15_min", "1_h", "2_h", "4_h"]:
    for delay in range(1, 17):
        path = "/Users/douglasbouchet/HXRO_ANN_Trader/prediction/" + timeframe
        os.system(
            f'cd {path} && grep -v "^T" trade_{delay}.csv > temp.csv && grep -v "^a" temp.csv > trade_{delay}.csv && rm temp.csv'
        )
