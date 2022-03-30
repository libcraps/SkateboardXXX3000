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
    if ("notTricks" in name) or ("fail" in name):
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

print(label)
dist_euc = np.array(dist_euc)
dist_euc_H1 = np.array(dist_euc_H1)
print(dist_euc.shape)

min_list = np.amin(dist_euc,axis=1)[:,0]
ind_list = np.argmin(dist_euc,axis=1)[:,0]

min_list_H1 = np.amin(dist_euc_H1,axis=1)[:,0]
ind_list_H1 = np.argmin(dist_euc_H1,axis=1)[:,0]


plt.hist(min_list, bins=15, color="r", alpha=0.8)
plt.hist(min_list_H1, bins=15, color="b", alpha=0.8)
plt.show()

print(ind_list)
print(Y)

print(Y==ind_list)

"""
dist_euc_shov_H1 = np.array(dist_euc_shov_H1)
dist_euc_ollie_H1 = np.array(dist_euc_ollie_H1)
dist_euc_kickflip_H1 = np.array(dist_euc_kickflip_H1)
dist_euc_treflip_H1 = np.array(dist_euc_treflip_H1)
dist_euc_heelflip_H1 = np.array(dist_euc_ollie_H1)
dist_euc_popshov_H1= np.array(dist_euc_popshov_H1)
min_dist_H1 = np.amin(np.array(
    [dist_euc_kickflip_H1, dist_euc_shov_H1, dist_euc_ollie_H1, dist_euc_heelflip_H1, dist_euc_treflip_H1, dist_euc_popshov_H1]),
    axis=0)
min_dist = np.amin(np.array([dist_euc_kickflip,dist_euc_shov,dist_euc_ollie,dist_euc_heelflip,dist_euc_treflip,dist_euc_popshov]), axis=0)
print(min_dist.shape)
plt.hist(dist_euc_kickflip[:,-2],alpha=0.7,bins=50)
plt.hist(min_dist[:,-2],bins=50,color="b")
plt.hist(min_dist_H1[:,-2],bins=50,color="r")
plt.show()


t = [i for i in range(len(trickDataSet.rawData["time"]))]
plt.plot(t,dist_df["gx"]*180/np.pi,"r")
plt.plot(t,dist_df["gy"]*180/np.pi,"green")
plt.plot(t,dist_df["gz"]*180/np.pi,"b")
plt.show()
print(dist_df)
"""

"""
for (repertoire, sousRepertoires, fichiers) in os.walk(tricksPath):
    if "OLD" not in repertoire:
        for file in fichiers:
            print(repertoire)
            f = os.path.join(repertoire, file)
            trickDataSet = sk.SkateboardXXX3000DataSet(f)
            Te = trickDataSet.Te

            dist_df = trickDataSet.rawData - ref_fs_shovit.rawData
            print(di)

"""
