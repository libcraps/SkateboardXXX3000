"""
Programs to compare different processed tricks

"""

import dataSet.SkateboardXXX3000DataSet as sk
import tools.FilterMethods as fm
import tools.integratinoFunctions as ef
import tools.signalAnalysis as sa
import tools.DisplayFunctions as df
import os
import numpy as np
import matplotlib.pyplot as plt


############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet
tricks="ollie"
folderPath_1 = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"+tricks+"_1_interpolated_processed.csv"
folderPath_2 = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"+tricks+"_2_interpolated_processed.csv"
folderPath_3 = "..\\..\\06 - Data\\Isolated_Tricks\\"+tricks+"\\"+tricks+"_3_interpolated_processed.csv"

folderPath_tricks = "..\\..\\06 - Data\\Isolated_Tricks\\360_flip\\360_flip_2_interpolated_processed.csv"

folderPath_ollie = "..\\..\\06 - Data\\Isolated_Tricks\\ollie\\ollie_1_interpolated_processed.csv"
folderPath_kickflip = "..\\..\\06 - Data\\Isolated_Tricks\\kickflip\\kickflip_1_interpolated_processed.csv"
folderPath_heelflip = "..\\..\\06 - Data\\Isolated_Tricks\\heelflip\\heelflip_1_interpolated_processed.csv"
folderPath_pop_shov = "..\\..\\06 - Data\\Isolated_Tricks\\pop_shovit\\pop_shovit_1_interpolated_processed.csv"
folderPath_fs_shov = "..\\..\\06 - Data\\Isolated_Tricks\\fs_shovit\\fs_shovit_1_interpolated_processed.csv"
folderPath_360_flip = "..\\..\\06 - Data\\Isolated_Tricks\\360_flip\\360_flip_1_interpolated_processed.csv"

# -------- Data processing ----------------------
dataSet_ollie = sk.SkateboardXXX3000DataSet(folderPath_ollie) #0
dataSet_kickflip = sk.SkateboardXXX3000DataSet(folderPath_kickflip) #1
dataSet_heelflip = sk.SkateboardXXX3000DataSet(folderPath_heelflip) #2
dataSet_pop_shov = sk.SkateboardXXX3000DataSet(folderPath_pop_shov) #3
dataSet_fs_shov = sk.SkateboardXXX3000DataSet(folderPath_fs_shov) #4
dataSet_360_flip = sk.SkateboardXXX3000DataSet(folderPath_360_flip) #5

dataSet_tricks = sk.SkateboardXXX3000DataSet(folderPath_tricks)
"""
sp_ollie = np.fft.fft(dataSet_kickflip.rawData["gx_normalized_1"], n=8*len(dataSet_kickflip.rawData["gx"]))
freq_ollie = np.fft.fftfreq(len(sp_ollie), 0.001/dataSet_kickflip.Te)
sp_heel = np.fft.fft(dataSet_heelflip.rawData["gx_normalized_1"], n=8*len(dataSet_heelflip.rawData["gx"]))
freq_heel = np.fft.fftfreq(len(sp_heel), 0.001/dataSet_heelflip.Te)
sp_360= np.fft.fft(dataSet_360_flip.rawData["gx_normalized_1"], n=8*len(dataSet_360_flip.rawData["gx"]))
freq_360= np.fft.fftfreq(len(sp_360), 0.001/dataSet_360_flip.Te)
plt.plot(freq_ollie,np.abs(sp_ollie), color="b")
plt.plot(freq_heel,np.abs(sp_heel), color="orange")
plt.plot(freq_360, np.abs(sp_360), color="black")
plt.show()
"""

"""
cor = {}
cor["cor_ollie"] = correlate_tricks(dataSet_tricks, dataSet_ollie)
cor["cor_kickflip"] = correlate_tricks(dataSet_tricks, dataSet_kickflip)
cor["cor_heelflip"] = correlate_tricks(dataSet_tricks, dataSet_heelflip)
cor["cor_pop_shovit"] = correlate_tricks(dataSet_tricks, dataSet_pop_shov)
cor["cor_fs_shovit"] = correlate_tricks(dataSet_tricks, dataSet_fs_shov)
cor["cor_360flip"] = correlate_tricks(dataSet_tricks, dataSet_360_flip)
"""
cor1 = sa.correlate_tricks(dataSet_tricks.rawData, dataSet_ollie.rawData)
cor2 = sa.correlate_tricks(dataSet_tricks.rawData, dataSet_kickflip.rawData)
cor3 = sa.correlate_tricks(dataSet_tricks.rawData, dataSet_heelflip.rawData)
cor4 = sa.correlate_tricks(dataSet_tricks.rawData, dataSet_pop_shov.rawData)
cor5 = sa.correlate_tricks(dataSet_tricks.rawData, dataSet_fs_shov.rawData)
cor6 = sa.correlate_tricks(dataSet_tricks.rawData, dataSet_360_flip.rawData)

print(cor1)
print(cor2)
print(cor3)
print(cor4)
print(cor5)
print(cor6)

correlation_list = np.array([cor1,cor2,cor3,cor4,cor5,cor6])
idx_max=idx = np.argmax(correlation_list)

index_max=[]
for k in range(len(cor1)):
    idx = np.argmax(correlation_list[:,k])
    index_max.append(idx)
cor_mean = np.mean(correlation_list, axis=1)

print("Tricks : ", os.path.basename(folderPath_tricks))
print("------------------")
print("Vote index : ",index_max)
print("Max de chez max : ", idx_max//6)
print("Mean index : ", cor_mean)
print("Mean cor : ", np.argmax(cor_mean))

#l = list(cor.keys())

"""
dataSet1 = sk.SkateboardXXX3000DataSet(folderPath_1) #0
dataSet2 = sk.SkateboardXXX3000DataSet(folderPath_2) #0
dataSet3 = sk.SkateboardXXX3000DataSet(folderPath_3) #0

normGyroscope = list(dataSet1.rawData["normGyr"])
time = list(dataSet1.rawData["time"])
# ---- Temps moyen de la norme du gyrosocpe ------
index_mean_loc = sa.mean_time(normGyroscope)
print("Index mean : " + str(index_mean_loc))
print("Time mean : " + str(time[index_mean_loc]))
normGyroscope = list(dataSet2.rawData["normGyr"])
time = list(dataSet2.rawData["time"])
# ---- Temps moyen de la norme du gyrosocpe ------
index_mean_loc = sa.mean_time(normGyroscope)
print("Index mean : " + str(index_mean_loc))
print("Time mean : " + str(time[index_mean_loc]))
normGyroscope = list(dataSet3.rawData["normGyr"])
time = list(dataSet3.rawData["time"])
# ---- Temps moyen de la norme du gyrosocpe ------
index_mean_loc = sa.mean_time(normGyroscope)
print("Index mean : " + str(index_mean_loc))
print("Time mean : " + str(time[index_mean_loc]))

dataSet1.time = list((dataSet1.rawData["time"]-8.2)/(8.85-8.2))
dataSet2.time = list((dataSet2.rawData["time"]-14.85)/(15.5-14.85))
dataSet3.time = list((dataSet3.rawData["time"]-5.5)/(6.1-5.5))


plt.subplot(321)
plt.plot(dataSet1.time, dataSet1.rawData["gx_normalized"], color="r")
plt.plot(dataSet1.time, dataSet1.rawData["gy_normalized"], color="g")
plt.plot(dataSet1.time, dataSet1.rawData["gz_normalized"], color="b")
plt.title("Gyroscope normalisée")
plt.subplot(323)
plt.plot(dataSet2.time, dataSet2.rawData["gx_normalized"], color="r")
plt.plot(dataSet2.time, dataSet2.rawData["gy_normalized"], color="g")
plt.plot(dataSet2.time, dataSet2.rawData["gz_normalized"], color="b")
plt.subplot(325)
plt.plot(dataSet3.time, dataSet3.rawData["gx_normalized"], color="r")
plt.plot(dataSet3.time, dataSet3.rawData["gy_normalized"], color="g")
plt.plot(dataSet3.time, dataSet3.rawData["gz_normalized"], color="b")

plt.subplot(322)
plt.title("Norme du gyroscope")
plt.plot(dataSet1.time, dataSet1.normGyroscope, color="black")
plt.subplot(324)
plt.plot(dataSet2.time, dataSet2.normGyroscope, color="black")
plt.subplot(326)
plt.plot(dataSet3.time, dataSet3.normGyroscope, color="black")
plt.show()

plt.subplot(311)
plt.plot(dataSet1.time, dataSet1.rawData["gx_normalized"], color="r", alpha=0.5)
plt.plot(dataSet2.time, dataSet2.rawData["gx_normalized"], color="r", alpha=0.5)
plt.plot(dataSet3.time, dataSet3.rawData["gx_normalized"], color="r", alpha=0.5)
plt.subplot(312)
plt.plot(dataSet3.time, dataSet3.rawData["gy_normalized"], color="g", alpha=0.5)
plt.plot(dataSet2.time, dataSet2.rawData["gy_normalized"], color="g", alpha=0.5)
plt.plot(dataSet1.time, dataSet1.rawData["gy_normalized"], color="g", alpha=0.5)
plt.subplot(313)
plt.plot(dataSet3.time, dataSet3.rawData["gz_normalized"], color="b", alpha=0.5)
plt.plot(dataSet1.time, dataSet1.rawData["gz_normalized"], color="b", alpha=0.5)
plt.plot(dataSet2.time, dataSet2.rawData["gz_normalized"], color="b", alpha=0.5)

plt.show()
plt.subplot(311)
plt.plot(dataSet1.rawData["gx_normalized"])
plt.plot(dataSet2.rawData["gx_normalized"])
plt.plot(dataSet3.rawData["gx_normalized"])
plt.subplot(312)
plt.plot(signal.correlate(dataSet1.rawData["gx_normalized"], dataSet2.rawData["gx_normalized"]), color="brown")
plt.plot(signal.correlate(dataSet1.rawData["gx_normalized"], dataSet3.rawData["gx_normalized"]), color="grey")
plt.subplot(313)
plt.plot(signal.correlate(dataSet1.rawData["ax_normalized"], dataSet2.rawData["ax_normalized"]), color="brown")
plt.plot(signal.correlate(dataSet1.rawData["ax_normalized"], dataSet3.rawData["ax_normalized"]), color="grey")
plt.show()
"""