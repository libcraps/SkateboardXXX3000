"""

"""
import dataSet.SkateboardXXX3000DataSet as sk
import tools.integratinoFunctions as ef
import tools.signalAnalysis as sa
import random
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import sklearn
from sklearn.metrics import precision_recall_curve


tricksPath = "..\\..\\06 - Data\\Isolated_tricks\\"
referenceTricksPath = "..\\..\\06 - Data\\Reference_tricks\\"

ref_360flip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "360_flip_reference.csv")
ref_ollie = sk.SkateboardXXX3000DataSet(referenceTricksPath + "ollie_reference.csv")
ref_kickflip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "kickflip_reference.csv")
ref_heelflip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "heelflip_reference.csv")
ref_pop_shovit = sk.SkateboardXXX3000DataSet(referenceTricksPath + "pop_shovit_reference.csv")
ref_fs_shovit = sk.SkateboardXXX3000DataSet(referenceTricksPath + "fs_shovit_reference.csv")


"""
trickDataSet = sk.SkateboardXXX3000DataSet(tricksPath)
Te = trickDataSet.Te
"""


def f1_score(precisions, recalls):
    mult = precisions * recalls
    add = precisions + recalls
    f1s = 2 * mult / add
    return f1s


def best_threshold(f1s, thresholds):
    threshold = thresholds[np.argmax(f1s)]
    return threshold


def area(precisions, recalls):
    auprc = 0
    auprc = np.trapz(precisions[::-1], recalls[::-1], dx=1.0)
    return auprc

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
    if ("notTricks" not in repertoire):
        if ("fail" not in repertoire):
            for file in fichiers:

                f = os.path.join(repertoire, file)
                trickDataSet = sk.SkateboardXXX3000DataSet(f)
                Te = trickDataSet.Te

                Y.append(0)

                tricksGyr_normalized = arrayGyrNormalize(trickDataSet.rawData)
                dist_euc_file = np.zeros(shape=(6, 1))
                dist_euc_file[4] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_ollie, axis=0))
                dist_euc_file[3] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_kickflip, axis=0))
                dist_euc_file[2] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_heelflip, axis=0))
                dist_euc_file[5] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_pop_shovit, axis=0))
                dist_euc_file[1] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_fs_shovit, axis=0))
                dist_euc_file[0] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_360Flip, axis=0))

                dist_euc.append(dist_euc_file)
    if ("notTricks" in repertoire):
        for file in fichiers:

            f = os.path.join(repertoire, file)
            trickDataSet = sk.SkateboardXXX3000DataSet(f)
            Te = trickDataSet.Te
            tricksGyr_normalized = arrayGyrNormalize(trickDataSet.rawData)
            dist_euc_file = np.zeros(shape=(6, 1))
            dist_euc_file[4] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_ollie, axis=0))
            dist_euc_file[3] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_kickflip, axis=0))
            dist_euc_file[2] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_heelflip, axis=0))
            dist_euc_file[5] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_pop_shovit, axis=0))
            dist_euc_file[1] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_fs_shovit, axis=0))
            dist_euc_file[0] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_360Flip, axis=0))

            dist_euc_H1.append(dist_euc_file)
            Y.append(1)

print(label)
dist_euc = np.array(dist_euc)
dist_euc_H1 = np.array(dist_euc_H1)
print(dist_euc.shape)

min_list = np.amin(dist_euc,axis=1)[:,0]
ind_list = np.argmin(dist_euc,axis=1)[:,0]

min_list_H1 = np.amin(dist_euc_H1,axis=1)[:,0]
ind_list_H1 = np.argmin(dist_euc_H1,axis=1)[:,0]


plt.hist(min_list, bins=15,  alpha=0.8, label="Tricks")
plt.hist(min_list_H1, bins=15, alpha=0.8, label="Not Tricks")
plt.title("Distance euclidienne minimum - Accélération")
plt.legend()
plt.xlabel("Valeurs minimums")
plt.ylabel("Fréquences")
plt.show()

Y_pred = np.concatenate([min_list, min_list_H1])
Y_true = np.concatenate([np.zeros(min_list.shape), np.ones(min_list_H1.shape)])
precisions, recalls, thresholds = precision_recall_curve(Y_true, Y_pred)


plt.figure(figsize=(4, 4))
plt.plot(recalls, precisions)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.xlim(0, 1.05)
plt.ylim(0, 1.05)
plt.grid(linestyle="--")
plt.title("ROC curve pour la distance euclidienne minim faites sur le gyroscope normalisé \n AUPCR : {}".format(round(area(precisions,recalls),5)))
plt.show()



f1s = f1_score(precisions,recalls)
best_f1_thresh = best_threshold(f1s, thresholds)
plt.plot(thresholds,f1s[:-1])
plt.plot(best_f1_thresh, np.amax(f1s),"r+--")
plt.title("Evolution du F1 score en fonction du seuil - Gyroscope normalisé \n F1 max pour seuil = {}".format(round(best_f1_thresh,2)))
plt.xlabel("Seuil")
plt.ylabel("f1 score")
plt.show()

print("Best F1 score : {}".format(round(np.amax(f1s),2)))
print("AUPCR : {}".format(round(area(precisions,recalls),2)))