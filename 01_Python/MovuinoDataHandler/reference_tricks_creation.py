import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import dataSet.SkateboardXXX3000DataSet as sk
import tools.display_functions as df
import tools.integratino_functions as i

tricks_name = "fs_shovit"
folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\" + tricks_name + "\\"
#folderPath = "..\\..\\06 - Data\\Raw_sequences\\"
#folderPath = "..\\..\\06 - Data\\Raw_Sequences\\sesh_190322\\"


i=1

for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    n=len(fichiers)
    random.shuffle(fichiers)
    mean_df = sk.SkateboardXXX3000DataSet(os.path.join(repertoire, fichiers[0])).rawData

    for file in fichiers[1:]:
        if "success" in file:
            if 1<=i<n:
                f = os.path.join(repertoire, file)
                skateDataSet = sk.SkateboardXXX3000DataSet(f)
                t = [i for i in range(len(skateDataSet.rawData["time"]))]
                #df.plotVector(t, np.array([skateDataSet.rawData["gx"], skateDataSet.rawData["gy"], skateDataSet.rawData["gz"]]).T*180/np.pi, "Acceleration", 111)
                mean_df = mean_df + skateDataSet.rawData

                i+=1

    #plt.show()

mean_df/=n
#mean_df.to_csv("..\\..\\06 - Data\\Reference_tricks\\" + tricks_name + "_reference.csv", sep=",", index=False, index_label=False)

plt.subplot(221)
plt.plot(t,mean_df["ax_normalized"],"r")
plt.plot(t,mean_df["ay_normalized"],"green")
plt.plot(t,mean_df["az_normalized"],"b")
plt.xlabel("Amplitude")
plt.ylabel("Points")
plt.title("Acceleration normalisée : {}".format(tricks_name))
plt.subplot(222)
plt.plot(t,mean_df["gx_normalized"],"r")
plt.plot(t,mean_df["gy_normalized"],"green")
plt.plot(t,mean_df["gz_normalized"],"b")
plt.xlabel("Amplitude")
plt.ylabel("Points")
plt.title("Gyroscope normalisé : {}".format(tricks_name))
plt.subplot(223)
plt.plot(t,mean_df["normAccel"],"black")
plt.title("Norme de l'accélération")
plt.xlabel("Amplitude")
plt.ylabel("Points")
plt.subplot(224)
plt.plot(t,mean_df["normGyr"],"black")
plt.title("Norme du gyroscope")
plt.xlabel("Amplitude")
plt.ylabel("Points")
plt.tight_layout()
plt.show()


