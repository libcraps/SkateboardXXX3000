"""
Program for the dataprocessing of isolated tricks

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

folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\ollie\\ollie_1.csv"
folderPath_2 = "..\\..\\06 - Data\\Isolated_Tricks\\ollie\\ollie_2.csv"

# -------- Data processing ----------------------

print("Processing : " + folderPath)
popShovDataSet = sk.SkateboardXXX3000DataSet(folderPath)
popShovDataSet_2 = sk.SkateboardXXX3000DataSet(folderPath_2)

nb_features_channel = 30
features = np.zeros((6, nb_features_channel))
features_2 = np.zeros((6, nb_features_channel))

def divide(lst, n):
    p = len(lst) // n
    if len(lst)-p > 0:
        return [lst[:p]] + divide(lst[p:], n-1)
    else:
        return [lst]

split_gyrX = divide(popShovDataSet.gyroscope[2,:],nb_features_channel)
split_gyrX_2 = divide(popShovDataSet_2.gyroscope[2,:],nb_features_channel)



"""
for i,l in enumerate(split_gyrX):
    features[3,i] = np.mean(l)


for i,l in enumerate(split_gyrX_2):
    features_2[3,i] = np.mean(l)
"""

size_window = 8
overlap = 4

features = sa.mean_moving_window(popShovDataSet.gyroscope[1,:], size_window, overlap)
features_2 = sa.mean_moving_window(popShovDataSet_2.gyroscope[1,:], size_window, overlap)
x = [k for k in range(len(features))]
width = 1
height = features
height_2 = features_2

plt.bar(x,height, width, alpha=0.5)
plt.bar(x,height_2, width,alpha=0.5)
plt.ylabel('Counts')
plt.title('Diagramme en Batons !')
plt.show()