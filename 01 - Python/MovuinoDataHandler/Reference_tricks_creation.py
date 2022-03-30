import dataSet.SkateboardXXX3000DataSet as sk
import os
import numpy as np
import matplotlib.pyplot as plt
import tools.displayFunctions as df
import tools.integratinoFunctions as i
import random
import pandas as pd

tricks_name = "fs_shovit"
folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\" + tricks_name + "\\"
#folderPath = "..\\..\\06 - Data\\Raw_sequences\\"
#folderPath = "..\\..\\06 - Data\\Raw_Sequences\\sesh_190322\\"


i=1

for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    n=len(fichiers)//2
    random.shuffle(fichiers)
    mean_df = sk.SkateboardXXX3000DataSet(os.path.join(repertoire, fichiers[0])).rawData
    for file in fichiers[1:]:
        if "success" in file:
            if 1<=i<n:
                f = os.path.join(repertoire, file)
                skateDataSet = sk.SkateboardXXX3000DataSet(f)
                t = [i for i in range(len(skateDataSet.rawData["time"]))]
                df.plotVector(t, np.array([skateDataSet.rawData["gx"], skateDataSet.rawData["gy"], skateDataSet.rawData["gz"]]).T*180/np.pi, "Acceleration", 111)
                mean_df = mean_df + skateDataSet.rawData

                i+=1

    plt.show()

mean_df/=n
mean_df.to_csv("..\\..\\06 - Data\\Reference_tricks\\" + tricks_name + "_reference.csv", sep=",", index=False, index_label=False)

plt.plot(t,mean_df["gx"]*180/np.pi,"r")
plt.plot(t,mean_df["gy"]*180/np.pi,"green")
plt.plot(t,mean_df["gz"]*180/np.pi,"b")
plt.show()

