import dataSet.SkateboardXXX3000DataSet as sk
import pandas as pd
import tools.signalAnalysis as sa
import tools.displayFunctions as df
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from scipy.signal import find_peaks


############   SETTINGS   #############
completeSequencesPath = "..\\..\\06 - Data\\Raw_sequences\\sesh_151121_\\record_9_interpolated.csv"
referenceTricksPath = "..\\..\\06 - Data\\Reference_tricks\\"

ref_360flip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "360_flip_reference.csv")
ref_ollie = sk.SkateboardXXX3000DataSet(referenceTricksPath + "ollie_reference.csv")
ref_kickflip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "kickflip_reference.csv")
ref_heelflip = sk.SkateboardXXX3000DataSet(referenceTricksPath + "heelflip_reference.csv")
ref_pop_shovit = sk.SkateboardXXX3000DataSet(referenceTricksPath + "pop_shovit_reference.csv")
ref_fs_shovit = sk.SkateboardXXX3000DataSet(referenceTricksPath + "fs_shovit_reference.csv")

def arrayGyrNormalize(rawData):
    return np.array([rawData["gx_normalized"], rawData["gy_normalized"], rawData["gz_normalized"]])

def Insert_row_(row_number, df, row_value):
    df2 = df[row_number:]
    df1 = df[0:row_number]
    df1.loc[0] = row_value
    df_result = pd.concat([df1, df2])
    df_result.index = [*range(df_result.shape[0])]
    return df_result

def correctionInterpolation(rawData):
    n = len(rawData["time"])
    # On s'assure qu'on a 120pt
    interpolateDf = rawData
    if n < 120:
        rawData["time"] = np.round(rawData["time"], 2)
        interpolateDf = sk.SkateboardXXX3000DataSet.interpolate_skate_data(rawData, 0.01)

        # interpolateDf.to_csv(f[:-4] + "_interpolated" + ".csv", sep=",", index=False, index_label=False)
        if len(interpolateDf["time"]) > 120:
            interpolateDf = interpolateDf.iloc[0:120, :]

        elif len(interpolateDf["time"]) < 120:
            k = 120 - len(interpolateDf["time"])
            df = interpolateDf.copy()
            for i in range(k):
                if i % 2 == 1:
                    temp = df["time"][0]
                    temp -= 0.01
                    df = Insert_row_(0, df, [temp,
                                             df["ax"][0],
                                             df["ay"][0],
                                             df["az"][0],
                                             df["gx"][0],
                                             df["gy"][0],
                                             df["gz"][0]])
                else:
                    temp = list(df["time"])[-1]
                    temp += 0.01
                    df = df.append({'time': temp,
                                    'ax': df["ax"][0],
                                    'ay': df["ay"][0],
                                    'az': df["az"][0],
                                    'gx': df["gx"][0],
                                    'gy': df["gy"][0],
                                    'gz': df["gz"][0]}, ignore_index=True)
                    df.index = [*range(df.shape[0])]
            interpolateDf = df
    elif n > 120:
        k = (n - 120) // 2
        interpolateDf = rawData.iloc[0:120, :]
    return interpolateDf

#--- Opening file ---
print("Opening : " + completeSequencesPath)
completeSequence = sk.SkateboardXXX3000DataSet(completeSequencesPath)
Te = completeSequence.Te
print("sample period : " + str(Te))
print("sample frequency : " + str(1 / Te))

#------- PEAK DETECTION ----------
size_window = int(1/Te)
overlap = int(size_window // 2)

prominence = 3
distance = 4

#----------------
#extract every event of the complete path
time_win, tricks_interval_temp, peaks_gyr, peaks_a, peaks_tricks = sa.eventDetection(completeSequence, size_window,overlap,prominence,distance)
events_interval = sa.centerEvents(completeSequence,  tricks_interval_temp)

#------------

seuil = 0.0121

gyrNormalize_360Flip = arrayGyrNormalize(ref_360flip.rawData)
gyrNormalize_ollie = arrayGyrNormalize(ref_ollie.rawData)
gyrNormalize_kickflip = arrayGyrNormalize(ref_kickflip.rawData)
gyrNormalize_heelflip = arrayGyrNormalize(ref_heelflip.rawData)
gyrNormalize_pop_shovit = arrayGyrNormalize(ref_pop_shovit.rawData)
gyrNormalize_fs_shovit = arrayGyrNormalize(ref_fs_shovit.rawData)

label=['360_flip', 'fs_shovit', 'heelflip', 'kickflip', 'ollie', 'pop_shovit','Not tricks']
Y_pred=[]

for i, interval in enumerate(events_interval):
    tricks = completeSequence.rawData.loc[interval[0]:interval[1], :]

    newDF = correctionInterpolation(tricks)
    newDF = sk.SkateboardXXX3000DataSet.normalizedL2(newDF.copy())

    #distance euclidienne
    tricksGyr_normalized = arrayGyrNormalize(newDF)
    dist_euc_file = np.zeros(shape=(6, 1))
    dist_euc_file[4] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_ollie, axis=0))
    dist_euc_file[3] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_kickflip, axis=0))
    dist_euc_file[2] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_heelflip, axis=0))
    dist_euc_file[5] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_pop_shovit, axis=0))
    dist_euc_file[1] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_fs_shovit, axis=0))
    dist_euc_file[0] = np.mean(np.linalg.norm(tricksGyr_normalized - gyrNormalize_360Flip, axis=0))

    minVal = np.amin(dist_euc_file)
    ind = np.argmin(dist_euc_file)
    #tricks pas tricks ?
    if minVal > seuil:
        Y_pred.append(len(label)-1)
    else :
        Y_pred.append(ind)

    #raté pas raté ?


plt.figure(figsize=(10,20))
time_list = np.array(completeSequence.time)

df.plotVect(time_list, completeSequence.acceleration, 'Acceleration (m/s2)', 221)
plt.xlabel("Temps (s)")
plt.legend(loc='upper right')
plt.grid()
plt.subplot(223)
plt.plot(time_list, completeSequence.normAcceleration, label='Norme Accélération', color="black")
plt.legend(loc='upper right')
plt.grid()
plt.show()
df.plotVect(time_list, completeSequence.gyroscope, 'Gyroscope (deg/s)', 211)

for i, interval in enumerate(events_interval):
    i_start = interval[0]
    i_end = interval[1]
    plt.plot(
        [completeSequence.time[i_start], completeSequence.time[i_start], completeSequence.time[i_end], completeSequence.time[i_end],
         completeSequence.time[i_start]], [-abs(max(completeSequence.normGyroscope[i_start:i_end])),
                                       abs(max(completeSequence.normGyroscope[i_start:i_end])),
                                       abs(max(completeSequence.normGyroscope[i_start:i_end])),
                                       -abs(max(completeSequence.normGyroscope[i_start:i_end])),
                                       -abs(max(completeSequence.normGyroscope[i_start:i_end]))], color="r")
    plt.text(completeSequence.time[i_start], max(completeSequence.normGyroscope[i_start:i_end])+50,"{}".format(label[Y_pred[i]],fontsize=20))
plt.legend(loc='upper right')
plt.xlabel("Temps (s)")
plt.grid()
plt.ylim([-max(completeSequence.normGyroscope)*1.2,max(completeSequence.normGyroscope)*1.2])
plt.subplot(212)
plt.plot(time_list, completeSequence.normGyroscope, label="Norme gyroscope", color="black")
plt.legend(loc='upper right')
plt.grid()
plt.show()
