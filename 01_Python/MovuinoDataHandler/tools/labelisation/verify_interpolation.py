"""
Program for event detection

"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

import movuinos.SkateboardXXX3000DataSet as sk
import tools.display_functions as df
import tools.signal_analysis as sa

from pathlib import Path

############   SETTINGS   #############
complete_sequences_path = Path("..\\..\\..\\..\\06_Data\\Raw_sequences\\sesh_160122")

print(complete_sequences_path.exists())
for path in complete_sequences_path.glob(pattern='*'):
    print(path)
    #--- Opening file ---
    print("Opening : " + path.name)
    complete_sequence = sk.SkateboardXXX3000DataSet(str(path))

    complete_sequence.rawData=complete_sequence.rawData.copy().round(4).drop_duplicates()

    complete_sequence.rawData.to_csv(path,index=False)
    complete_sequence = sk.SkateboardXXX3000DataSet(str(path))
    """
    skateDataSet.time =[t/1000 for t in skateDataSet.time]
    skateDataSet.interpolateData["time"] /=1000
    Te = skateDataSet.Te/1000
    """
    Te = complete_sequence.Te
    print("sample period : " + str(Te))
    print("sample frequency : " + str(1 / Te))

    list_dt = [complete_sequence.time[i] - complete_sequence.time[i - 1] for i in range(1, complete_sequence.nb_row)]
    ecart_min = min(list_dt)
    list_dt=np.pad(list_dt, (1,0))
    plt.plot(complete_sequence.time, list_dt)
    plt.title("Sample rate evolution")
    plt.ylabel("dt (s)")
    plt.xlabel("Time (s)")
    plt.show()
