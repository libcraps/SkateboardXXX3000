import dataSet.SkateboardXXX3000DataSet as sk
import pandas as pd
import tools.signalAnalysis as sa
import tools.displayFunctions as df
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from scipy.signal import find_peaks


############   SETTINGS   #############
completeSequencesPath = "..\\..\\06 - Data\\Raw_sequences\\sesh_151121_\\record_9_interpolated.csv"
referenceTricksPath = "..\\..\\06 - Data\\Reference_tricks\\"

#--- Opening file ---
print("Opening : " + completeSequencesPath)
completeSequence = sk.SkateboardXXX3000DataSet(completeSequencesPath)
Te = completeSequence.Te
print("sample period : " + str(Te))
print("sample frequency : " + str(1 / Te))

#------- PEAK DETECTION ----------
size_window = int(1/Te)
overlap = int(size_window // 2)

prominence = 3
distance = 4

#----------------
#extract every event of the complete path
time_win, tricks_interval_temp, peaks_gyr, peak_a, peaks_tricks = sa.eventDetection(completeSequence, size_window,overlap,prominence,distance)
events_interval = sa.centerEvents(completeSequence,  tricks_interval_temp)

#------------



for i, interval in enumerate(events_interval):
    tricks = completeSequence.rawData.loc[interval[0]:interval[1], :]
    tricks = sk.SkateboardXXX3000DataSet.normalizedL2(tricks.copy())
    #distance euclidienne

    #tricks pas tricks ?

    #raté pas raté ?
