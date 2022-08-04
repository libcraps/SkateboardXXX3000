import os

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import movuinos.SkateboardXXX3000DataSet as sk

############   SETTINGS   #############
device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "..\\..\\06_Data\\sequences\\sesh_300722\\"
Path(folderPath).mkdir(exist_ok=True)
gen_filename = "record"  # generic name, numbers will be added for duplicates

serialPort = 'COM6'

# --------- Data Extraction from Movuino ----------

print("data extraction")
sk.SkateboardXXX3000DataSet.movuinoExtraction(serialPort, folderPath, gen_filename)

# --------- Interpolation of data -----------------

for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    for file in fichiers:
        f = os.path.join(repertoire, file)
        print(f)
        skateDataSet = sk.SkateboardXXX3000DataSet(f)
        """
        if skateDataSet.Te>10:
            print("milli")
            skateDataSet.time = [t/1000 for t in skateDataSet.time]
            skateDataSet.rawData["time"] = skateDataSet.time
            skateDataSet.rawData.to_csv(f, sep=",", index=False, index_label=False)
        elif skateDataSet.Te<0.001:
            skateDataSet.time = [t * 1000 for t in skateDataSet.time]
            skateDataSet.rawData["time"] = skateDataSet.time
            skateDataSet.rawData.to_csv(f, sep=",", index=False, index_label=False)
        """
        interpolateDf = sk.SkateboardXXX3000DataSet.interpolate_skate_data(skateDataSet.rawData,0.01)
        interpolateDf.to_csv(f[:-4] + "_interpolated" +".csv", sep=",", index=False, index_label=False)
