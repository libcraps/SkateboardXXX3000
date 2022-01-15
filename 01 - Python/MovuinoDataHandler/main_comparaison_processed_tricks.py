"""
Programs to compare different processed tricks

"""

import dataSet.SkateboardXXX3000DataSet as sk
import tools.FilterMethods as fm
import tools.integratinoFunctions as ef
import tools.signalAnalysis as sa
import tools.DisplayFunctions as df
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet
tricks="ollie"
folderPath_1 = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"+tricks+"_1_treated.csv"
folderPath_2 = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"+tricks+"_2_treated.csv"
folderPath_3 = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"+tricks+"_3_treated.csv"

# -------- Data processing ----------------------

print("Processing : " + folderPath_1)
dataSet1 = sk.SkateboardXXX3000DataSet(folderPath_1)
print("Processing : " + folderPath_2)
dataSet2 = sk.SkateboardXXX3000DataSet(folderPath_2)
print("Processing : " + folderPath_3)
dataSet3 = sk.SkateboardXXX3000DataSet(folderPath_3)
"""
dataSet1.time = list((dataSet1.rawData["time"]-8.2)/(8.85-8.2))
dataSet2.time = list((dataSet2.rawData["time"]-14.85)/(15.5-14.85))
dataSet3.time = list((dataSet3.rawData["time"]-5.5)/(6.1-5.5))
"""
plt.subplot(321)
plt.plot(dataSet1.time, dataSet1.rawData["gx_normalized"], color="r")
plt.plot(dataSet1.time, dataSet1.rawData["gy_normalized"], color="g")
plt.plot(dataSet1.time, dataSet1.rawData["gz_normalized"], color="b")
plt.subplot(323)
plt.plot(dataSet2.time, dataSet2.rawData["gx_normalized"], color="r")
plt.plot(dataSet2.time, dataSet2.rawData["gy_normalized"], color="g")
plt.plot(dataSet2.time, dataSet2.rawData["gz_normalized"], color="b")
plt.subplot(325)
plt.plot(dataSet3.time, dataSet3.rawData["gx_normalized"], color="r")
plt.plot(dataSet3.time, dataSet3.rawData["gy_normalized"], color="g")
plt.plot(dataSet3.time, dataSet3.rawData["gz_normalized"], color="b")

plt.subplot(322)
plt.plot(dataSet1.time, dataSet1.normGyroscope, color="black")
plt.subplot(324)
plt.plot(dataSet2.time, dataSet2.normGyroscope, color="black")
plt.subplot(326)
plt.plot(dataSet3.time, dataSet3.normGyroscope, color="black")
plt.show()

plt.subplot(311)
plt.plot(dataSet1.time, dataSet1.rawData["gx_normalized"], color="r", alpha=0.5)
plt.plot(dataSet2.time, dataSet2.rawData["gx_normalized"], color="r", alpha=0.5)
plt.plot(dataSet3.time, dataSet3.rawData["gx_normalized"], color="r", alpha=0.5)
plt.subplot(312)
plt.plot(dataSet3.time, dataSet3.rawData["gy_normalized"], color="g", alpha=0.5)
plt.plot(dataSet2.time, dataSet2.rawData["gy_normalized"], color="g", alpha=0.5)
plt.plot(dataSet1.time, dataSet1.rawData["gy_normalized"], color="g", alpha=0.5)
plt.subplot(313)
plt.plot(dataSet3.time, dataSet3.rawData["gz_normalized"], color="b", alpha=0.5)
plt.plot(dataSet1.time, dataSet1.rawData["gz_normalized"], color="b", alpha=0.5)
plt.plot(dataSet2.time, dataSet2.rawData["gz_normalized"], color="b", alpha=0.5)

plt.show()
plt.subplot(311)
plt.plot(dataSet1.rawData["gx_normalized"])
plt.plot(dataSet2.rawData["gx_normalized"])
plt.plot(dataSet3.rawData["gx_normalized"])
plt.subplot(312)
plt.plot(signal.correlate(dataSet1.rawData["gx_normalized"], dataSet2.rawData["gx_normalized"]), color="brown")
plt.plot(signal.correlate(dataSet1.rawData["gx_normalized"], dataSet3.rawData["gx_normalized"]), color="grey")
plt.subplot(313)
plt.plot(signal.correlate(dataSet1.rawData["ax_normalized"], dataSet2.rawData["ax_normalized"]), color="brown")
plt.plot(signal.correlate(dataSet1.rawData["ax_normalized"], dataSet3.rawData["ax_normalized"]), color="grey")
plt.show()

f, t, Sxx = signal.spectrogram(dataSet1.rawData["gx_normalized"], 1000, nperseg=4)
print(Sxx)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()