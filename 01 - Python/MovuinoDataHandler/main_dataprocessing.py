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
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\"
filename = "record"  # generic name numbers will be added for duplicates

filter = 20

# -------- Data processing ----------------------

listeFichiers = []

for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    for file in fichiers:
        if "interpolated" in file:
            f = os.path.join(repertoire, file)
            skateDataSet = sk.SkateboardXXX3000DataSet(f)
            Te = skateDataSet.Te

            print("sample frequency : " + str(1 / Te))

            #Normalizatio of the data
            airG=np.trapz(skateDataSet.normGyroscope, skateDataSet.time)
            airA=np.trapz(skateDataSet.normAcceleration, skateDataSet.time)

            skateDataSet.rawData['ax_normalized'] = skateDataSet.rawData['ax']/airA
            skateDataSet.rawData['ay_normalized'] = skateDataSet.rawData['ay']/airA
            skateDataSet.rawData['az_normalized'] = skateDataSet.rawData['az']/airA

            skateDataSet.rawData['gx_normalized'] = skateDataSet.rawData['gx']/airG
            skateDataSet.rawData['gy_normalized'] = skateDataSet.rawData['gy']/airG
            skateDataSet.rawData['gz_normalized'] = skateDataSet.rawData['gz']/airG

            skateDataSet.rawData['ax_normalized_1'] = skateDataSet.rawData['ax']/np.amax(abs(skateDataSet.rawData['ax']))
            skateDataSet.rawData['ay_normalized_1'] = skateDataSet.rawData['ay']/np.amax(abs(skateDataSet.rawData['ay']))
            skateDataSet.rawData['az_normalized_1'] = skateDataSet.rawData['az']/np.amax(abs(skateDataSet.rawData['az']))

            skateDataSet.rawData['gx_normalized_1'] = skateDataSet.rawData['gx']/np.amax(abs(skateDataSet.rawData['gx']))
            skateDataSet.rawData['gy_normalized_1'] = skateDataSet.rawData['gy']/np.amax(abs(skateDataSet.rawData['gy']))
            skateDataSet.rawData['gz_normalized_1'] = skateDataSet.rawData['gz']/np.amax(abs(skateDataSet.rawData['gz']))

            # Stock in processed.csv
            #skateDataSet.rawData.to_csv(f[:-4] + "_processed.csv", sep=",", index=False, index_label=False)




