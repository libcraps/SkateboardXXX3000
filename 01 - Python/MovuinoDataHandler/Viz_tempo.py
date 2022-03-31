"""
Fichier qui sert a sortir les figures manquantes du rapport
"""

import os
import dataSet.SkateboardXXX3000DataSet as sk
import tools.displayFunctions as df
import numpy as np
import matplotlib.pyplot as plt
import random

tricks="notTricks"
folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"
i=0
for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    random.shuffle(fichiers)
    for file in fichiers:
        if i < 10:
            print(repertoire)
            f = os.path.join(repertoire, file)
            skateDataSet = sk.SkateboardXXX3000DataSet(f)
            skateDataSet.dispRawData()
            i+=1



