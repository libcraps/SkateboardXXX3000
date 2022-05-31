"""

"""
import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.metrics as mt
from scipy import signal
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

import dataSet.SkateboardXXX3000DataSet as sk
import tools.integratino_functions as ef
import tools.signal_analysis as sa

tricksPath = "..\\..\\06 - Data\\Isolated_tricks\\"
referenceTricksPath = "..\\..\\06 - Data\\Reference_tricks\\"

ref_360flip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "360_flip_reference.csv")
ref_ollie = sk.SkateboardXXX3000DataSet(referenceTricksPath + "ollie_reference.csv")
ref_kickflip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "kickflip_reference.csv")
ref_heelflip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "heelflip_reference.csv")
ref_pop_shovit = sk.SkateboardXXX3000DataSet(referenceTricksPath + "pop_shovit_reference.csv")
ref_fs_shovit = sk.SkateboardXXX3000DataSet(referenceTricksPath + "fs_shovit_reference.csv")

def arrayGyrNormalize(rawData):
    return np.array([rawData["gx_normalized"], rawData["gy_normalized"], rawData["gz_normalized"]])

def arrayAccNormalize(rawData):
    return np.array([rawData["ax_normalized"], rawData["ay_normalized"], rawData["az_normalized"]])


gyrNormalize_360Flip = arrayGyrNormalize(ref_360flip.rawData)
gyrNormalize_ollie = arrayGyrNormalize(ref_ollie.rawData)
gyrNormalize_kickflip = arrayGyrNormalize(ref_kickflip.rawData)
gyrNormalize_heelflip = arrayGyrNormalize(ref_heelflip.rawData)
gyrNormalize_pop_shovit = arrayGyrNormalize(ref_pop_shovit.rawData)
gyrNormalize_fs_shovit = arrayGyrNormalize(ref_fs_shovit.rawData)


dist_euc = []
dist_euc_H1 = []

Y=[]
label=[]
for (repertoire, sousRepertoires, fichiers) in os.walk(tricksPath):
            label.append(sousRepertoires)

label = label[0]
for i,name in enumerate(label) :
    if ("fail" in name) or ("notTricks" in name):
        del label[i]


for (repertoire, sousRepertoires, fichiers) in os.walk(tricksPath):
    if ("notTricks" not in repertoire):
        if ("fail" not in repertoire):
            for file in fichiers:

                f = os.path.join(repertoire, file)
                trickDataSet = sk.SkateboardXXX3000DataSet(f)
                Te = trickDataSet.Te

                for i,name in enumerate(label):
                    if name in file:
                        Y.append(i)

                tricksGyr_normalized = arrayGyrNormalize(trickDataSet.rawData)
                dist_euc_file = np.zeros(shape=(6, 1))
                dist_euc_file[4] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_ollie, axis=0))
                dist_euc_file[3] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_kickflip, axis=0))
                dist_euc_file[2] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_heelflip, axis=0))
                dist_euc_file[5] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_pop_shovit, axis=0))
                dist_euc_file[1] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_fs_shovit, axis=0))
                dist_euc_file[0] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_360Flip, axis=0))

                dist_euc.append(dist_euc_file)

print(label)
dist_euc = np.array(dist_euc)

print(dist_euc.shape)

min_list = np.amin(dist_euc,axis=1)[:,0]
ind_list = np.argmin(dist_euc,axis=1)[:,0]

plt.hist(min_list, bins=15,  alpha=0.8, label="Tricks")
plt.title("Distance euclidienne minimum - Accélération")
plt.legend()
plt.xlabel("Valeurs minimums")
plt.ylabel("Fréquences")
plt.show()

print(ind_list)
print(Y)

print(Y==ind_list)

print(confusion_matrix(Y,ind_list))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

array = confusion_matrix(Y,ind_list)

disp = ConfusionMatrixDisplay(confusion_matrix=array,
                          display_labels=label)

disp.plot(cmap="gray")
plt.title("Confusion matrix - tricks classification")
plt.show()

print(mt.accuracy_score(Y,ind_list))

precisionScore_sklearn_microavg = mt.precision_score(Y, ind_list, average='micro')
#
# Average is assigned macro
#
precisionScore_sklearn_macroavg = mt.precision_score(Y, ind_list, average='macro')

precisionScore_sklearn_weightedavg = mt.precision_score(Y, ind_list, average='weighted')

print(precisionScore_sklearn_macroavg)
print(precisionScore_sklearn_microavg)
print(precisionScore_sklearn_weightedavg)