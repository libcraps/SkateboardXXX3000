"""
Fichier qui sert a sortir les figures manquantes du rapport
"""

import os
import dataSet.SkateboardXXX3000DataSet as sk
import tools.displayFunctions as df
import numpy as np
import matplotlib.pyplot as plt

tricks="ollie"
folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"
i=0
for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    for file in fichiers:
        if i < 2:
            print(repertoire)
            f = os.path.join(repertoire, file)
            skateDataSet = sk.SkateboardXXX3000DataSet(f)
            t = [i for i in range(len(skateDataSet.rawData["time"]))]
            df.plotVector(t, np.array([skateDataSet.rawData["gx_normalized"], skateDataSet.rawData["gy_normalized"], skateDataSet.rawData["gz_normalized"]]).T, "Gyroscope normalisée"*(i==0), 211+i)
            i+=1
plt.show()


