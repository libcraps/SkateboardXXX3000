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

folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\heelflip\\"
filename = "record"  # generic name numbers will be added for duplicates

filter = 20

# -------- Data processing ----------------------

listeFichiers = []
for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    for file in fichiers:
        if "treated" not in file:
            filepath = folderPath + file
            skateDataSet = sk.SkateboardXXX3000DataSet(filepath)
            Te = skateDataSet.Te

            print("sample frequency : " + str(1 / Te))

            #Normalizatio of the data
            airG=0
            airA=0
            for k in range(len(skateDataSet.time)-1):
                dt=skateDataSet.time[k+1]-skateDataSet.time[k]
                airG+=(skateDataSet.normGyroscope[k+1]+skateDataSet.normGyroscope[k])*dt/2
                airA+=(skateDataSet.normAcceleration[k+1]+skateDataSet.normAcceleration[k])*dt/2

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

            """
            skateDataSet.rawData['ax_normalized'] = skateDataSet.rawData['ax']/np.sum(skateDataSet.normAcceleration)
            skateDataSet.rawData['ay_normalized'] = skateDataSet.rawData['ay']/np.sum(skateDataSet.normAcceleration)
            skateDataSet.rawData['az_normalized'] = skateDataSet.rawData['az']/np.sum(skateDataSet.normAcceleration)
            
            skateDataSet.rawData['gx_normalized'] = skateDataSet.rawData['gx']/np.sum(skateDataSet.normGyroscope)
            skateDataSet.rawData['gy_normalized'] = skateDataSet.rawData['gy']/np.sum(skateDataSet.normGyroscope)
            skateDataSet.rawData['gz_normalized'] = skateDataSet.rawData['gz']/np.sum(skateDataSet.normGyroscope)
            """
            # Filtering
            skateDataSet.acceleration_lp = fm.MeanFilter(skateDataSet.acceleration, filter)
            skateDataSet.gyroscope_lp = fm.MeanFilter(skateDataSet.gyroscope, filter)

            # Integration of values :
            skateDataSet.velocity = ef.EulerIntegration(skateDataSet.acceleration, Te)
            skateDataSet.ThetaGyr = ef.EulerIntegration(skateDataSet.gyroscope, Te)
            skateDataSet.pos = ef.EulerIntegration(skateDataSet.velocity, Te)

            # Stock in processed.csv
            skateDataSet.stockProcessedData(filepath[:-4] + "_treated.csv")




