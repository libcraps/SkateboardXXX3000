import dataSet.SkateboardXXX3000DataSet as sk
import pandas as pd
import tools.signalAnalysis as sa
import os
import matplotlib.pyplot as plt
import tools.DisplayFunctions as df
import numpy as np
############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

completeSequencesPath = "..\\..\\06 - Data\\Isolated_Tricks\\ollie\\ollie_1.csv"
print("Opening : " + completeSequencesPath)
skateDataSet = sk.SkateboardXXX3000DataSet(completeSequencesPath)
skateDataSet.time =[t/1000 for t in skateDataSet.time]
skateDataSet.rawData["time"] /=1000
Te = skateDataSet.Te
print("sample frequency : " + str(1 / Te))

skateDataSet.gyroscope -= np.mean(skateDataSet.gyroscope, axis=0)

plt.subplot(221)
plt.plot(skateDataSet.gyroscope[:,0],skateDataSet.gyroscope[:,1], 'ob')
plt.title("gy = f(gx)")
plt.grid()
plt.subplot(222)
plt.plot(skateDataSet.gyroscope[:,0],skateDataSet.gyroscope[:,2], 'og')
plt.title("gz = f(gx)")
plt.grid()
plt.subplot(223)
plt.plot(skateDataSet.gyroscope[:,1],skateDataSet.gyroscope[:,2], 'or')
plt.title("gz = f(gy)")
plt.grid()
plt.subplot(224)
df.PlotVector(skateDataSet.time, skateDataSet.gyroscope, 'Gyroscope (deg/s)', 224)
plt.grid()
plt.show()