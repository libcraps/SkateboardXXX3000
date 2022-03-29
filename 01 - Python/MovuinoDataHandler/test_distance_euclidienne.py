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

dist_euc_shov=[]
dist_euc_ollie=[]
dist_euc_kickflip=[]
dist_euc_treflip=[]
dist_euc_heelflip=[]
dist_euc_popshov=[]


dist_euc_shov_H1=[]
dist_euc_ollie_H1=[]
dist_euc_kickflip_H1=[]
dist_euc_treflip_H1=[]
dist_euc_heelflip_H1=[]
dist_euc_popshov_H1=[]

for (repertoire, sousRepertoires, fichiers) in os.walk(tricksPath):
    if ("notTricks" not in repertoire) or ("fail" not in repertoire):
        for file in fichiers:
            print(repertoire)
            f = os.path.join(repertoire, file)
            trickDataSet = sk.SkateboardXXX3000DataSet(f)
            Te = trickDataSet.Te

            dist_euc_shov.append(np.linalg.norm(trickDataSet.rawData - ref_fs_shovit.rawData, axis=0)[1:15])
            dist_euc_ollie.append(np.linalg.norm(trickDataSet.rawData - ref_ollie.rawData, axis=0)[1:15])
            dist_euc_kickflip.append(np.linalg.norm(trickDataSet.rawData - ref_kickflip.rawData, axis=0)[1:15])
            dist_euc_popshov.append(np.linalg.norm(trickDataSet.rawData - ref_pop_shovit.rawData, axis=0)[1:15])
            dist_euc_heelflip.append(np.linalg.norm(trickDataSet.rawData - ref_heelflip.rawData, axis=0)[1:15])
            dist_euc_treflip.append(np.linalg.norm(trickDataSet.rawData - ref_360flip.rawData, axis=0)[1:15])

    if "notTricks" in repertoire:
        for file in fichiers:
            print(repertoire)
            f = os.path.join(repertoire, file)
            trickDataSet = sk.SkateboardXXX3000DataSet(f)
            Te = trickDataSet.Te

            dist_euc_shov_H1.append(np.linalg.norm(trickDataSet.rawData - ref_fs_shovit.rawData, axis=0)[1:15])
            dist_euc_ollie_H1.append(np.linalg.norm(trickDataSet.rawData - ref_ollie.rawData, axis=0)[1:15])
            dist_euc_kickflip_H1.append(np.linalg.norm(trickDataSet.rawData - ref_kickflip.rawData, axis=0)[1:15])
            dist_euc_popshov_H1.append(np.linalg.norm(trickDataSet.rawData - ref_pop_shovit.rawData, axis=0)[1:15])
            dist_euc_heelflip_H1.append(np.linalg.norm(trickDataSet.rawData - ref_heelflip.rawData, axis=0)[1:15])
            dist_euc_treflip_H1.append(np.linalg.norm(trickDataSet.rawData - ref_360flip.rawData, axis=0)[1:15])


dist_euc_shov = np.array(dist_euc_shov)
dist_euc_ollie = np.array(dist_euc_ollie)
dist_euc_kickflip = np.array(dist_euc_kickflip)
dist_euc_treflip = np.array(dist_euc_treflip)
dist_euc_heelflip = np.array(dist_euc_ollie)
dist_euc_popshov= np.array(dist_euc_popshov)


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
plt.hist(dist_euc_ollie[:,-2],alpha=0.7,bins=50)
plt.hist(dist_euc_shov[:,-2],alpha=0.7,bins=50)
plt.hist(dist_euc_popshov[:,-2],alpha=0.7,bins=50)
plt.hist(dist_euc_treflip[:,-2],alpha=0.7,bins=50)
plt.hist(dist_euc_heelflip[:,-2],alpha=0.7,bins=50)
plt.hist(min_dist[:,-2],bins=50,color="b")
plt.hist(min_dist_H1[:,-2],bins=50,color="r")
plt.show()

"""
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
