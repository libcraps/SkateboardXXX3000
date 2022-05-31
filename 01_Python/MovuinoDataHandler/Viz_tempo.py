"""
Fichier qui sert a sortir les figures manquantes du rapport
"""

import os
import random

import matplotlib.pyplot as plt
import numpy as np

import dataSet.SkateboardXXX3000DataSet as sk
import tools.display_functions as df

tricks="kickflip"
tricks="pop_shovit"
folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"

referenceTricksPath = "..\\..\\06 - Data\\Reference_tricks\\"

ref_360flip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "360_flip_reference.csv")
ref_ollie = sk.SkateboardXXX3000DataSet(referenceTricksPath + "ollie_reference.csv")
ref_kickflip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "kickflip_reference.csv")
ref_heelflip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "heelflip_reference.csv")
ref_pop_shovit = sk.SkateboardXXX3000DataSet(referenceTricksPath + "pop_shovit_reference.csv")
ref_fs_shovit = sk.SkateboardXXX3000DataSet(referenceTricksPath + "fs_shovit_reference.csv")


def arrayGyrNormalize(rawData):
    return np.array([rawData["gx_normalized"], rawData["gy_normalized"], rawData["gz_normalized"]])


gyrNormalize_360Flip = arrayGyrNormalize(ref_360flip.rawData)
gyrNormalize_ollie = arrayGyrNormalize(ref_ollie.rawData)
gyrNormalize_kickflip = arrayGyrNormalize(ref_kickflip.rawData)
gyrNormalize_heelflip = arrayGyrNormalize(ref_heelflip.rawData)
gyrNormalize_pop_shovit = arrayGyrNormalize(ref_pop_shovit.rawData)
gyrNormalize_fs_shovit = arrayGyrNormalize(ref_fs_shovit.rawData)


i=0
for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    random.shuffle(fichiers)
    for file in fichiers:
        if i < 1:
            print(repertoire)
            f = os.path.join(repertoire, file)
            skateDataSet = sk.SkateboardXXX3000DataSet(f)
            #skateDataSet.dispRawData()
            i+=1


lim_x = [-0.04,0.04]
lim_y = [-0.065,0.03]
lim_z = [-0.04,0.04]

plt.subplot(331)
plt.plot(skateDataSet.rawData["gx_normalized"],color="red")
plt.title(tricks)
plt.ylabel("Amplitude")
plt.grid()
plt.ylim(lim_x)
plt.subplot(334)
plt.plot(skateDataSet.rawData["gy_normalized"],color="green")
plt.ylabel("Amplitude")
plt.grid()
plt.ylim(lim_y)
plt.subplot(337)
plt.plot(skateDataSet.rawData["gz_normalized"],color="blue")
plt.xlabel("Temps")
plt.ylabel("Amplitude")
plt.ylim(lim_z)
plt.grid()

plt.subplot(332)
plt.plot(gyrNormalize_kickflip[0],color="red")
plt.title("Figure de référence : kickflip")
plt.ylim(lim_x)
plt.grid()
plt.subplot(335)
plt.plot(gyrNormalize_kickflip[1],color="green")
plt.grid()
plt.ylim(lim_y)
plt.subplot(338)
plt.plot(gyrNormalize_kickflip[2],color="blue")
plt.xlabel("Temps")
plt.ylim(lim_z)
plt.grid()


plt.subplot(333)
plt.plot(np.abs(gyrNormalize_kickflip[0]-skateDataSet.rawData["gx_normalized"]),color="red")
plt.title("Comparaison des 3 canaux (x,y,z) entre \n le pop_shovit et le kickflip de référence")
plt.grid()
plt.ylim([-0.01,0.05])
plt.subplot(336)
plt.plot(np.abs(gyrNormalize_kickflip[1]-skateDataSet.rawData["gy_normalized"]),color="green")
plt.grid()
plt.ylim([-0.01,0.05])
plt.subplot(339)
plt.plot(np.abs(gyrNormalize_kickflip[2]-skateDataSet.rawData["gz_normalized"]),color="blue")
plt.grid()
plt.ylim([-0.01,0.075])
plt.xlabel("Temps")
plt.show()
"""
plt.subplot(321)
plt.plot(skateDataSet.acceleration[:,0])

"""


