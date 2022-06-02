"""
Program for event detection

"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

import movuinos.SkateboardXXX3000DataSet as sk
import tools.display_functions as df
import tools.signal_analysis as sa

############   SETTINGS   #############
complete_sequences_path = "..\\..\\06_Data\\Raw_sequences\\sesh_151121_\\record_7_interpolated.csv"


#--- Opening file ---
print("Opening : " + complete_sequences_path)
complete_sequence = sk.SkateboardXXX3000DataSet(complete_sequences_path)

"""
skateDataSet.time =[t/1000 for t in skateDataSet.time]
skateDataSet.interpolateData["time"] /=1000
Te = skateDataSet.Te/1000
"""
Te = complete_sequence.Te
print("sample period : " + str(Te))
print("sample frequency : " + str(1 / Te))

list_dt = [complete_sequence.time[i] - complete_sequence.time[i - 1] for i in range(1, complete_sequence.nb_row)]
ecart_min = min(list_dt)
list_dt=np.pad(list_dt, (1,0))
plt.plot(complete_sequence.time, list_dt)
plt.title("Sample rate evolution")
plt.ylabel("dt (s)")
plt.xlabel("Time (s)")
plt.show()

#------- PEAK DETECTION ----------
size_window = int(1/Te)
overlap = int(size_window // 2)

prominence = 3
distance = 3

#--------------------------------
if size_window%2 == 0 :
    size_window+=1

window = [0, size_window]
retard = size_window // 2

sum_acc = []
sum_gyr = []

time_win = []

output = []

normAcc = np.pad(complete_sequence.normAcceleration, (int(size_window // 2), int(size_window // 2)))
normGyr = np.pad(complete_sequence.normGyroscope, (int(size_window // 2), int(size_window // 2)))

while window[1] < len(complete_sequence.time):
    time_win.append(complete_sequence.time[(window[0] + window[1]) // 2 - retard])
    sum_acc.append(np.mean(normAcc[window[0]:window[1]]))
    sum_gyr.append(np.mean(normGyr[window[0]:window[1]]))

    window[0] += size_window - overlap
    window[1] += size_window - overlap

sum_gyr = np.array(sum_gyr)
sum_acc = np.array(sum_acc)
peaks_gyr, _gyr = find_peaks(sum_gyr, prominence=prominence, distance=distance)
peaks_acc, _acc = find_peaks(sum_acc, prominence=prominence-1, distance=distance-2)
time_win = np.array(time_win)

peaks_tricks = []
delta_peak = 2

for i,peak_a in enumerate(peaks_acc):
    for j,peak_g in enumerate(peaks_gyr):
        if peak_g-delta_peak < peak_a < peak_g+delta_peak:
            peaks_tricks.append(peak_g)

dt_i = 0.8
dt_f = 0.6

tricks_interval = []
for i in peaks_tricks:
    if time_win[i]-dt_i < 0 :
        tricks_interval.append([0.1, time_win[i] + dt_i])
    else:
        tricks_interval.append([time_win[i]-dt_i, time_win[i]+dt_i])

#skateDataSet.dispRawData()
time_list = np.array(complete_sequence.time)
df.plotVect(time_list, complete_sequence.acceleration, 'Acceleration (m/s2)', 321)
plt.plot(time_win,sum_acc,'-o', markersize=2, color="grey")
plt.plot(time_win[peaks_acc], sum_acc[peaks_acc], "v", markersize=5, color="orange", label="Peaks")
plt.plot(time_win[peaks_tricks], sum_acc[peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
plt.xlabel("Temps (s)")
plt.legend(loc='upper right')
plt.grid()
plt.subplot(323)
plt.plot(time_list, complete_sequence.normAcceleration, label='Norme Accélération', color="black")
plt.legend(loc='upper right')
plt.grid()
plt.subplot(325)
plt.plot(time_win,sum_acc,'-o', markersize=2)
plt.plot(time_win[peaks_acc], sum_acc[peaks_acc], "v", markersize=5, color="orange", label="Peaks")
plt.plot(time_win[peaks_tricks], sum_acc[peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
plt.title("Norme de l'accélération fenêtrée")
plt.grid()
df.plotVect(time_list, complete_sequence.gyroscope, 'Gyroscope (deg/s)', 322)
plt.plot(time_win, sum_gyr,'-o', markersize=2, color="grey")
plt.plot(time_win[peaks_gyr], sum_gyr[peaks_gyr], "v", markersize=5, color="orange", label="Peaks")
plt.plot(time_win[peaks_tricks], sum_gyr[peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
plt.legend(loc='upper right')
plt.xlabel("Temps (s)")
plt.grid()
plt.subplot(324)
plt.plot(time_list, complete_sequence.normGyroscope, label="Norme gyroscope", color="black")
plt.legend(loc='upper right')
plt.grid()

plt.subplot(326)
plt.plot(time_win, sum_gyr,'-o', markersize=2)
plt.plot(time_win[peaks_gyr], sum_gyr[peaks_gyr], "v", markersize=5, color="orange", label="Peaks")
plt.plot(time_win[peaks_tricks], sum_gyr[peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
plt.title("Norme du gyroscope fenêtrée")

plt.grid()
plt.tight_layout()
plt.show()

#------------ PEAKS ISOLATION ------------------

for k in range(len(tricks_interval)):
    #We're looking for the best index that matches with the time interval
    i_start = int(float(tricks_interval[k][0]-0.1)/Te)
    i_end = int(float(tricks_interval[k][1]-0.1)/Te)

    while complete_sequence.time[i_start] < tricks_interval[k][0]:
        i_start += 1

    while complete_sequence.time[i_end] < tricks_interval[k][1]:
        i_end += 1

    print("Tricks' start time : " + str(complete_sequence.time[i_start]))
    print("Tricks' end time : " + str(complete_sequence.time[i_end]))

    df_iso_tricks = complete_sequence.interpolateData.iloc[i_start:i_end, :]

    normGyroscope = list(df_iso_tricks["normGyr"])
    time = list(df_iso_tricks["time"])

    # ---- Temps moyen de la norme du gyrosocpe ------
    index_mean_loc = sa.mean_time(normGyroscope)
    print("Index mean : " + str(index_mean_loc))
    print("Mean time  : " + str(complete_sequence.time[i_start] + index_mean_loc * Te))


    #teeest :
    #g = np.cumsum(skateDataSet.normGyroscope[i_start:i_end])
    #index_mean_loc = np.argmin(np.abs(g - np.amax(g) / 2))
    print("Index mean : " + str(index_mean_loc))
    mean_time = complete_sequence.time[i_start] + index_mean_loc * Te

    new_tricks_interval = [mean_time-dt_f, mean_time+dt_f]
    i_start=0
    i_end=0
    while complete_sequence.time[i_start] < new_tricks_interval[0]:
        i_start += 1

    while complete_sequence.time[i_end] < new_tricks_interval[1]:
        i_end += 1


    print("Tricks' start time : " + str(complete_sequence.time[i_start]))
    print("Tricks' end time : " + str(complete_sequence.time[i_end]))
    print("Simpler : [ {} , {}]".format(complete_sequence.time[int(float(mean_time - dt_f) / Te) - 1], complete_sequence.time[int(float(mean_time + dt_f) / Te) + 1]))

    time_list = complete_sequence.time[i_start:i_end]



    plt.subplot(321)
    df.plotVect(complete_sequence.time, complete_sequence.acceleration, 'Acceleration (m/s2)', 321)
    plt.plot(
        [complete_sequence.time[i_start], complete_sequence.time[i_start], complete_sequence.time[i_end], complete_sequence.time[i_end],
         complete_sequence.time[i_start]], [-abs(max(complete_sequence.normAcceleration[i_start:i_end])),
                                            abs(max(complete_sequence.normAcceleration[i_start:i_end])),
                                            abs(max(complete_sequence.normAcceleration[i_start:i_end])),
                                            -abs(max(complete_sequence.normAcceleration[i_start:i_end])),
                                            -abs(max(complete_sequence.normAcceleration[i_start:i_end]))], color="r")
    plt.subplot(322)
    df.plotVect(complete_sequence.time, complete_sequence.gyroscope, 'Gyroscope (deg/s)', 322)
    plt.plot(
        [complete_sequence.time[i_start], complete_sequence.time[i_start], complete_sequence.time[i_end], complete_sequence.time[i_end],
         complete_sequence.time[i_start]], [-abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                            abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                            abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                            -abs(max(complete_sequence.normGyroscope[i_start:i_end])),
                                            -abs(max(complete_sequence.normGyroscope[i_start:i_end]))], color="r")
    plt.subplot(323)
    df.plotVect(time_list, complete_sequence.acceleration[:, i_start:i_end], 'Acceleration (m/s2)', 323)
    plt.legend(loc='upper right')
    plt.subplot(325)
    plt.plot(time_list, complete_sequence.normAcceleration[i_start:i_end], '-x', label='Norme Accélération', color="black")
    plt.legend(loc='upper right')
    plt.subplot(324)
    df.plotVect(time_list, complete_sequence.gyroscope[:, i_start:i_end], 'Gyroscope (deg/s)', 324)
    plt.legend(loc='upper right')
    plt.subplot(326)
    plt.plot(time_list, complete_sequence.normGyroscope[i_start:i_end], '-x', label="Norme gyroscope", color="black")
    plt.legend(loc='upper right')
    plt.grid()
    plt.tight_layout()
    plt.show()
    """
    g=np.cumsum(skateDataSet.normGyroscope[i_start:i_end])
    print(max(g))
    print(skateDataSet.time[i_start +np.argmin(np.abs(g-np.amax(g)/2))])
    plt.plot(g)
    plt.plot([0, 120],[np.amax(g)/2, np.amax(g)/2],'r+--')
    plt.plot([np.argmin(np.abs(g-np.amax(g)/2)), np.argmin(np.abs(g-np.amax(g)/2))],[0, np.amax(g)],'r+--')
    plt.show()

    plt.plot(np.abs(g-np.amax(g)/2))
    plt.show()
    """


#---- File extraction ----
    toExtract = str(input("Voulez vous extraire les données d'une figure y/n - other (o):"))

    if toExtract == "y":
        # Tricks to isolate
        tricks_name = str(input("Quelle figure voulez vous extraitre (ollie, kickflip, heelflip, pop_shovit, fs_shovit, 360_flip, fs_180, bs_180, notTricks) :"))
        isSuccess = str(input("Est ce que la figure est réussi y/n - other (o):"))
        succes = "success"
        if isSuccess == "n":
            succes = "fail"

        listeFichiers = []
        for (repertoire, sousRepertoires, fichiers) in os.walk("..\\..\\06 - Data\\Isolated_Tricks\\" + tricks_name + "\\"):
            listeFichiers.extend(fichiers)
        fileTricksPath = "..\\..\\06 - Data\\Isolated_Tricks\\" + tricks_name + "\\" + tricks_name + "_" + succes + "_"+str(len(listeFichiers)+1) + ".csv"

        df_iso_tricks = complete_sequence.rawData.iloc[i_start:i_end, :]

        dir = os.path.dirname(fileTricksPath)
        if not os.path.exists(dir):
            os.makedirs(dir)
        df_iso_tricks.to_csv(fileTricksPath, sep=",", index=False, index_label=False)

        tricks = sk.SkateboardXXX3000DataSet(fileTricksPath)
