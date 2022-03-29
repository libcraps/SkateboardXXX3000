"""
Program for the dataprocessing of isolated tricks

"""

import dataSet.SkateboardXXX3000DataSet as sk
import tools.integratinoFunctions as ef
import tools.signalAnalysis as sa
import tools.displayFunctions as df
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
liste_len=[]
liste_dt=[]
err=[]
for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    if "OLD" not in repertoire:
        for file in fichiers:
            print(repertoire)
            f = os.path.join(repertoire, file)
            skateDataSet = sk.SkateboardXXX3000DataSet(f)
            Te = skateDataSet.Te

            print("sample frequency : " + str(1 / Te))
            skateDataSet.rawData = sk.SkateboardXXX3000DataSet.normalizedL2(skateDataSet.rawData)
            liste_dt.append(list(skateDataSet.rawData["time"])[-1]-skateDataSet.rawData["time"][0])
            liste_len.append(len(skateDataSet.rawData["time"]))
            if liste_len[-1]<1.15:
                err.append(file)


            # Stock in processed.csv
            #skateDataSet.rawData.to_csv(f, sep=",", index=False, index_label=False)


print(liste_len)
print(liste_dt)

print(np.round(skateDataSet.rawData["time"],2))