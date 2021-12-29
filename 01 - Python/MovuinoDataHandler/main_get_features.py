"""
Program for the dataprocessing of isolated tricks

"""

import dataSet.SkateboardXXX3000DataSet as sk
import tools.FilterMethods as fm
import tools.integratinoFunctions as ef
import tools.signalAnalysis as sa
import tools.DisplayFunctions as df
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath_ollie = "..\\..\\06 - Data\\Isolated_Tricks\\ollie\\ollie_1_treated.csv"
folderPath_kickflip = "..\\..\\06 - Data\\Isolated_Tricks\\kickflip\\kickflip_1_treated.csv"
folderPath_pop = "..\\..\\06 - Data\\Isolated_Tricks\\pop_shovit\\pop_shovit_1_treated.csv"

# -------- Data processing ----------------------

print("Processing : " + folderPath_ollie)
ollieDataSet = sk.SkateboardXXX3000DataSet(folderPath_ollie)
print("Processing : " + folderPath_kickflip)
kickflipDataSet = sk.SkateboardXXX3000DataSet(folderPath_kickflip)
print("Processing : " + folderPath_pop)
popShovDataSet = sk.SkateboardXXX3000DataSet(folderPath_pop)

print(ollieDataSet.rawData.columns)

dt_ollie = ollieDataSet.time[-1]-ollieDataSet.time[0]
dt_kick = kickflipDataSet.time[-1]-kickflipDataSet.time[0]
dt_pop = popShovDataSet.time[-1]-popShovDataSet.time[0]

print(len(ollieDataSet.time))
print(len(kickflipDataSet.time))
print(len(popShovDataSet.time))

featuresOllie = {}
featuresKick = {}
featuresPop = {}
"""
featuresOllie["Mean_ax"] = np.sum(ollieDataSet.rawData["ax_normalized"])/dt_ollie
featuresOllie["Mean_ay"] = np.sum(ollieDataSet.rawData["ay_normalized"])/dt_ollie
featuresOllie["Mean_az"] = np.sum(ollieDataSet.rawData["az_normalized"])/dt_ollie
featuresOllie["Mean_gx"] = np.sum(ollieDataSet.rawData["gx_normalized"])/dt_ollie
featuresOllie["Mean_gy"] = np.sum(ollieDataSet.rawData["gy_normalized"])/dt_ollie
featuresOllie["Mean_gz"] = np.sum(ollieDataSet.rawData["gz_normalized"])/dt_ollie

featuresOllie["std_ax"] = np.sum(featuresOllie["Mean_ax"]-ollieDataSet.rawData["ax_normalized"])/dt_ollie
featuresOllie["std_ay"] = np.sum(featuresOllie["Mean_ay"]-ollieDataSet.rawData["ay_normalized"])/dt_ollie
featuresOllie["std_az"] = np.sum(featuresOllie["Mean_az"]-ollieDataSet.rawData["az_normalized"])/dt_ollie
featuresOllie["std_gx"] = np.sum(featuresOllie["Mean_gx"]-ollieDataSet.rawData["gx_normalized"])/dt_ollie
featuresOllie["std_gy"] = np.sum(featuresOllie["Mean_gy"]-ollieDataSet.rawData["gy_normalized"])/dt_ollie
featuresOllie["std_gz"] = np.sum(featuresOllie["Mean_gz"]-ollieDataSet.rawData["gz_normalized"])/dt_ollie

featuresKick["Mean_ax"] = np.sum(kickflipDataSet.rawData["ax_normalized"])/dt_kick
featuresKick["Mean_ay"] = np.sum(kickflipDataSet.rawData["ay_normalized"])/dt_kick
featuresKick["Mean_az"] = np.sum(kickflipDataSet.rawData["az_normalized"])/dt_kick
featuresKick["Mean_gx"] = np.sum(kickflipDataSet.rawData["gx_normalized"])/dt_kick
featuresKick["Mean_gy"] = np.sum(kickflipDataSet.rawData["gy_normalized"])/dt_kick
featuresKick["Mean_gz"] = np.sum(kickflipDataSet.rawData["gz_normalized"])/dt_kick

featuresKick["std_ax"] = np.sum(featuresKick["Mean_ax"]-kickflipDataSet.rawData["ax_normalized"])/dt_kick
featuresKick["std_ay"] = np.sum(featuresKick["Mean_ay"]-kickflipDataSet.rawData["ay_normalized"])/dt_kick
featuresKick["std_az"] = np.sum(featuresKick["Mean_az"]-kickflipDataSet.rawData["az_normalized"])/dt_kick
featuresKick["std_gx"] = np.sum(featuresKick["Mean_gx"]-kickflipDataSet.rawData["gx_normalized"])/dt_kick
featuresKick["std_gy"] = np.sum(featuresKick["Mean_gy"]-kickflipDataSet.rawData["gy_normalized"])/dt_kick
featuresKick["std_gz"] = np.sum(featuresKick["Mean_gz"]-kickflipDataSet.rawData["gz_normalized"])/dt_kick

featuresPop["Mean_ax"] = np.sum(popShovDataSet.rawData["ax_normalized"])/dt_pop
featuresPop["Mean_ay"] = np.sum(popShovDataSet.rawData["ay_normalized"])/dt_pop
featuresPop["Mean_az"] = np.sum(popShovDataSet.rawData["az_normalized"])/dt_pop
featuresPop["Mean_gx"] = np.sum(popShovDataSet.rawData["gx_normalized"])/dt_pop
featuresPop["Mean_gy"] = np.sum(popShovDataSet.rawData["gy_normalized"])/dt_pop
featuresPop["Mean_gz"] = np.sum(popShovDataSet.rawData["gz_normalized"])/dt_pop

featuresPop["std_ax"] = np.sum(featuresPop["Mean_ax"]-popShovDataSet.rawData["ax_normalized"])/dt_pop
featuresPop["std_ay"] = np.sum(featuresPop["Mean_ay"]-popShovDataSet.rawData["ay_normalized"])/dt_pop
featuresPop["std_az"] = np.sum(featuresPop["Mean_az"]-popShovDataSet.rawData["az_normalized"])/dt_pop
featuresPop["std_gx"] = np.sum(featuresPop["Mean_gx"]-popShovDataSet.rawData["gx_normalized"])/dt_pop
featuresPop["std_gy"] = np.sum(featuresPop["Mean_gy"]-popShovDataSet.rawData["gy_normalized"])/dt_pop
featuresPop["std_gz"] = np.sum(featuresPop["Mean_gz"]-popShovDataSet.rawData["gz_normalized"])/dt_pop
"""

featuresOllie["Mean_ax"] = np.mean(ollieDataSet.rawData["ax_normalized"])
featuresOllie["Mean_ay"] = np.mean(ollieDataSet.rawData["ay_normalized"])
featuresOllie["Mean_az"] = np.mean(ollieDataSet.rawData["az_normalized"])
featuresOllie["Mean_gx"] = np.mean(ollieDataSet.rawData["gx_normalized"])
featuresOllie["Mean_gy"] = np.mean(ollieDataSet.rawData["gy_normalized"])
featuresOllie["Mean_gz"] = np.mean(ollieDataSet.rawData["gz_normalized"])

featuresOllie["std_ax"] = np.mean(featuresOllie["Mean_ax"]-ollieDataSet.rawData["ax_normalized"])/dt_ollie
featuresOllie["std_ay"] = np.mean(featuresOllie["Mean_ay"]-ollieDataSet.rawData["ay_normalized"])/dt_ollie
featuresOllie["std_az"] = np.mean(featuresOllie["Mean_az"]-ollieDataSet.rawData["az_normalized"])/dt_ollie
featuresOllie["std_gx"] = np.mean(featuresOllie["Mean_gx"]-ollieDataSet.rawData["gx_normalized"])/dt_ollie
featuresOllie["std_gy"] = np.mean(featuresOllie["Mean_gy"]-ollieDataSet.rawData["gy_normalized"])/dt_ollie
featuresOllie["std_gz"] = np.mean(featuresOllie["Mean_gz"]-ollieDataSet.rawData["gz_normalized"])/dt_ollie

featuresKick["Mean_ax"] = np.mean(kickflipDataSet.rawData["ax_normalized"])
featuresKick["Mean_ay"] = np.mean(kickflipDataSet.rawData["ay_normalized"])
featuresKick["Mean_az"] = np.mean(kickflipDataSet.rawData["az_normalized"])
featuresKick["Mean_gx"] = np.mean(kickflipDataSet.rawData["gx_normalized"])
featuresKick["Mean_gy"] = np.mean(kickflipDataSet.rawData["gy_normalized"])
featuresKick["Mean_gz"] = np.mean(kickflipDataSet.rawData["gz_normalized"])

featuresKick["std_ax"] = np.mean(featuresKick["Mean_ax"]-kickflipDataSet.rawData["ax_normalized"])
featuresKick["std_ay"] = np.mean(featuresKick["Mean_ay"]-kickflipDataSet.rawData["ay_normalized"])
featuresKick["std_az"] = np.mean(featuresKick["Mean_az"]-kickflipDataSet.rawData["az_normalized"])
featuresKick["std_gx"] = np.mean(featuresKick["Mean_gx"]-kickflipDataSet.rawData["gx_normalized"])
featuresKick["std_gy"] = np.mean(featuresKick["Mean_gy"]-kickflipDataSet.rawData["gy_normalized"])
featuresKick["std_gz"] = np.mean(featuresKick["Mean_gz"]-kickflipDataSet.rawData["gz_normalized"])

featuresPop["Mean_ax"] = np.mean(popShovDataSet.rawData["ax_normalized"])
featuresPop["Mean_ay"] = np.mean(popShovDataSet.rawData["ay_normalized"])
featuresPop["Mean_az"] = np.mean(popShovDataSet.rawData["az_normalized"])
featuresPop["Mean_gx"] = np.mean(popShovDataSet.rawData["gx_normalized"])
featuresPop["Mean_gy"] = np.mean(popShovDataSet.rawData["gy_normalized"])
featuresPop["Mean_gz"] = np.mean(popShovDataSet.rawData["gz_normalized"])

featuresPop["std_ax"] = np.mean(featuresPop["Mean_ax"]-popShovDataSet.rawData["ax_normalized"])
featuresPop["std_ay"] = np.mean(featuresPop["Mean_ay"]-popShovDataSet.rawData["ay_normalized"])
featuresPop["std_az"] = np.mean(featuresPop["Mean_az"]-popShovDataSet.rawData["az_normalized"])
featuresPop["std_gx"] = np.mean(featuresPop["Mean_gx"]-popShovDataSet.rawData["gx_normalized"])
featuresPop["std_gy"] = np.mean(featuresPop["Mean_gy"]-popShovDataSet.rawData["gy_normalized"])
featuresPop["std_gz"] = np.mean(featuresPop["Mean_gz"]-popShovDataSet.rawData["gz_normalized"])

plt.plot(kickflipDataSet.time, kickflipDataSet.rawData["gx_normalized"], color="r")
plt.plot(kickflipDataSet.time, kickflipDataSet.rawData["gy_normalized"], color="g")
plt.plot(kickflipDataSet.time, kickflipDataSet.rawData["gz_normalized"], color="b")
plt.show()

plt.subplot(321)
plt.bar(["Mean_ax","Mean_ay","Mean_az"], [featuresOllie["Mean_ax"],featuresOllie["Mean_ay"],featuresOllie["Mean_az"]], color=['r','g','b'])
plt.title("Ollie")
plt.grid()
plt.subplot(323)
plt.bar(["Mean_ax","Mean_ay","Mean_az"], [featuresKick["Mean_ax"],featuresKick["Mean_ay"],featuresKick["Mean_az"]], color=['r','g','b'])
plt.title("Kickflip")
plt.grid()
plt.subplot(325)
plt.bar(["Mean_ax","Mean_ay","Mean_az"], [featuresPop["Mean_ax"],featuresPop["Mean_ay"],featuresPop["Mean_az"]], color=['r','g','b'])
plt.title("PopShovit")
plt.grid()
plt.subplot(322)
plt.bar(["Mean_gx","Mean_gy","Mean_gz"], [featuresOllie["Mean_gx"],featuresOllie["Mean_gy"],featuresOllie["Mean_gz"]], color=['r','g','b'])
plt.title("Ollie")
plt.grid()
plt.subplot(324)
plt.bar(["Mean_gx","Mean_gy","Mean_gz"], [featuresKick["Mean_gx"],featuresKick["Mean_gy"],featuresKick["Mean_gz"]], color=['r','g','b'])
plt.title("Kickflip")
plt.grid()
plt.subplot(326)
plt.bar(["Mean_gx","Mean_gy","Mean_gz"], [featuresPop["Mean_gx"],featuresPop["Mean_gy"],featuresPop["Mean_gz"]], color=['r','g','b'])
plt.title("PopShovit")
plt.grid()
plt.tight_layout()
plt.show()

plt.subplot(321)
plt.bar(["std_ax","std_ay","std_az"], [featuresOllie["std_ax"],featuresOllie["std_ay"],featuresOllie["std_az"]], color=['r','g','b'])
plt.title("Ollie")
plt.grid()
plt.subplot(323)
plt.bar(["std_ax","std_ay","std_az"], [featuresKick["std_ax"],featuresKick["std_ay"],featuresKick["std_az"]], color=['r','g','b'])
plt.title("Kickflip")
plt.grid()
plt.subplot(325)
plt.bar(["std_ax","std_ay","std_az"], [featuresPop["std_ax"],featuresPop["std_ay"],featuresPop["std_az"]], color=['r','g','b'])
plt.title("PopShovit")
plt.grid()
plt.subplot(322)
plt.bar(["std_gx","std_gy","std_gz"], [featuresOllie["std_gx"],featuresOllie["std_gy"],featuresOllie["std_gz"]], color=['r','g','b'])
plt.title("Ollie")
plt.grid()
plt.subplot(324)
plt.bar(["std_gx","std_gy","std_gz"], [featuresKick["std_gx"],featuresKick["std_gy"],featuresKick["std_gz"]], color=['r','g','b'])
plt.title("Kickflip")
plt.grid()
plt.subplot(326)
plt.bar(["std_gx","std_gy","std_gz"], [featuresPop["std_gx"],featuresPop["std_gy"],featuresPop["std_gz"]], color=['r','g','b'])
plt.title("PopShovit")
plt.grid()
plt.tight_layout()
plt.show()


"""
plt.subplot(311)
plt.bar(featuresOllie.keys(), featuresOllie.values(), color=['r','g','b','r','g','b'])
plt.title("Ollie")
plt.grid()
plt.subplot(312)
plt.bar(featuresKick.keys(), featuresKick.values(), color=['r','g','b','r','g','b'])
plt.title("Kickflip")
plt.grid()
plt.subplot(313)
plt.bar(featuresPop.keys(), featuresPop.values(), color=['r','g','b','r','g','b'])
plt.title("PopShovit")
plt.grid()
plt.show()
"""


