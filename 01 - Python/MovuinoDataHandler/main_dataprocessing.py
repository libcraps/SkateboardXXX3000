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
filename = "record"  # generic name numbers will be added for duplicates

filter = 20

# -------- Data processing ----------------------

print("Processing : " + folderPath)
skateDataSet = sk.SkateboardXXX3000DataSet(folderPath)
Te = skateDataSet.Te

print("sample frequency : " + str(1 / Te))
# Filtering
skateDataSet.acceleration_lp = fm.MeanFilter(skateDataSet.acceleration, filter)
skateDataSet.gyroscope_lp = fm.MeanFilter(skateDataSet.gyroscope, filter)

# Integration of values :
skateDataSet.velocity = ef.EulerIntegration(skateDataSet.acceleration, Te)
skateDataSet.ThetaGyr = ef.EulerIntegration(skateDataSet.gyroscope, Te)
skateDataSet.pos = ef.EulerIntegration(skateDataSet.velocity, Te)

#Normalizatio of the data
for column in skateDataSet.rawData.columns:
    if column != "time" or "filter" in column:
        skateDataSet.rawData[column + '_normalized'] = sa.normalizeDat(skateDataSet.rawData[column])

# Stock in processed.csv
skateDataSet.stockProcessedData(folderPath[:-4] + "_treated.csv")



