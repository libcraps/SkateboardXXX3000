"""
Program for event detection

"""

import dataSet.SkateboardXXX3000DataSet as sk
import pandas as pd
import tools.signalAnalysis as sa
import tools.DisplayFunctions as df
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from scipy.signal import find_peaks
############   SETTINGS   #############
completeSequencesPath = "..\\..\\06 - Data\\Raw_sequences\\sesh_160122\\record_3_interpolated.csv"


#--- Opening file ---
print("Opening : " + completeSequencesPath)
skateDataSet = sk.SkateboardXXX3000DataSet(completeSequencesPath)

"""
skateDataSet.time =[t/1000 for t in skateDataSet.time]
skateDataSet.interpolateData["time"] /=1000
Te = skateDataSet.Te/1000
"""
Te = skateDataSet.Te
print("sample period : " + str(Te))
print("sample frequency : " + str(1 / Te))

#------- PEAK DETECTION ----------
size_window = int(1/Te)
overlap = int(size_window // 2)

if size_window%2 == 0 :
    size_window+=1

window = [0, size_window]
retard = size_window // 2

sum_acc = []
sum_gyr = []

time_win = []

#----Evolution du temps d'aquisition----

list_dt = [skateDataSet.time[i]-skateDataSet.time[i-1] for i in range(1,skateDataSet.nb_row)]
ecart_min = min(list_dt)
list_dt=np.pad(list_dt, (1,0))
plt.plot(skateDataSet.time,list_dt)
plt.title("Sample rate evolution")
plt.ylabel("dt (s)")
plt.xlabel("Time (s)")
plt.show()

ecart_min = round(ecart_min*1000)/1000

#-------------------------------------

normAcc = np.pad(skateDataSet.normAcceleration, (int(size_window // 2), int(size_window // 2)))
normGyr = np.pad(skateDataSet.normGyroscope, (int(size_window // 2), int(size_window // 2)))

while window[1] < len(skateDataSet.time):
    time_win.append(skateDataSet.time[(window[0]+window[1])//2 - retard])
    sum_acc.append(np.mean(normAcc[window[0]:window[1]]))
    sum_gyr.append(np.mean(normGyr[window[0]:window[1]]))

    window[0] += size_window - overlap
    window[1] += size_window - overlap

sum_gyr = np.array(sum_gyr)
sum_acc = np.array(sum_acc)
peaks_gyr, _gyr = find_peaks(sum_gyr, prominence=10, distance=10)
peaks_acc, _acc = find_peaks(sum_acc, prominence=3, distance=10)
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
time_list = np.array(skateDataSet.time)
df.plotVect(time_list, skateDataSet.acceleration, 'Acceleration (m/s2)', 321)
plt.plot(time_win,sum_acc,'-o', markersize=2, color="grey")
plt.plot(time_win[peaks_acc], sum_acc[peaks_acc], "v", markersize=5, color="orange", label="Peaks")
plt.plot(time_win[peaks_tricks], sum_acc[peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
plt.xlabel("Temps (s)")
plt.legend(loc='upper right')
plt.grid()
plt.subplot(323)
plt.plot(time_list, skateDataSet.normAcceleration, label='Norme Accélération', color="black")
plt.legend(loc='upper right')
plt.grid()
plt.subplot(325)
plt.plot(time_win,sum_acc,'-o', markersize=2)
plt.plot(time_win[peaks_acc], sum_acc[peaks_acc], "v", markersize=5, color="orange", label="Peaks")
plt.plot(time_win[peaks_tricks], sum_acc[peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
plt.title("Norme de l'accélération fenêtrée")
plt.grid()
df.plotVect(time_list, skateDataSet.gyroscope, 'Gyroscope (deg/s)', 322)
plt.plot(time_win, sum_gyr,'-o', markersize=2, color="grey")
plt.plot(time_win[peaks_gyr], sum_gyr[peaks_gyr], "v", markersize=5, color="orange", label="Peaks")
plt.plot(time_win[peaks_tricks], sum_gyr[peaks_tricks], "v", markersize=5, color="red", label="Peaks tricks")
plt.legend(loc='upper right')
plt.xlabel("Temps (s)")
plt.grid()
plt.subplot(324)
plt.plot(time_list, skateDataSet.normGyroscope, label="Norme gyroscope", color="black")
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
    #We're looking for the best index that mathces with the time interval
    i_start = int(float(tricks_interval[k][0]-0.1)/Te)
    i_end = int(float(tricks_interval[k][1]-0.1)/Te)

    while skateDataSet.time[i_start] < tricks_interval[k][0]:
        print(skateDataSet.time[i_start], tricks_interval[k][0])
        i_start += 1

    while skateDataSet.time[i_end] < tricks_interval[k][1]:
        i_end += 1

    print("Tricks' start time : " + str(skateDataSet.time[i_start]))
    print("Tricks' end time : " + str(skateDataSet.time[i_end]))

    df_iso_tricks = skateDataSet.interpolateData.iloc[i_start:i_end,:]

    normGyroscope = list(df_iso_tricks["normGyr"])
    time = list(df_iso_tricks["time"])

    # ---- Temps moyen de la norme du gyrosocpe ------
    index_mean_loc = sa.mean_time(normGyroscope)
    print("Index mean : " + str(index_mean_loc))
    print("Mean time  : " + str(skateDataSet.time[i_start] + index_mean_loc*Te))


    mean_time = skateDataSet.time[i_start] + index_mean_loc*Te

    """
    #TO KEEP
    index_mean_glob = 0
    size = 20 #nb points

    while skateDataSet.time[index_mean_glob] < mean_time:
        index_mean_glob += 1
    new_tricks_interval = [index_mean_glob, index_mean_glob]

    #left
    i_rl = index_mean_loc
    i_ll = index_mean_loc-size

    #right
    i_lr = index_mean_loc
    i_rr = index_mean_loc+size

    i_end = index_mean_glob

    eps = 75

    while sa.areaUnderCurve(time[i_ll:i_rl], normGyroscope[i_ll:i_rl]) > eps and i_ll >= 0:
        i_rl=i_ll
        i_ll=i_ll-size
        print("###" +str(i_ll))
    i_start_tricks = i_ll

    while sa.areaUnderCurve(time[i_lr:i_rr], normGyroscope[i_lr:i_rr]) > eps and i_rr<=len(time):
        print(i_start + i_lr)
        print("zzzzo " +str(sa.areaUnderCurve(time[i_lr:i_rr], normGyroscope[i_lr:i_rr])))
        i_lr=i_rr
        i_rr=i_ll+size
    i_end_tricks = i_rr
    print("zzzzo " + str(sa.areaUnderCurve(time[i_lr:i_rr], normGyroscope[i_lr:i_rr])))
    print("i_start_tricks " +str(i_start_tricks))
    print("i_end_tricks " +str(i_end_tricks))

    i_start = i_start+i_start_tricks
    i_end = i_end+i_end_tricks
    """

    new_tricks_interval = [mean_time-dt_f, mean_time+dt_f]
    i_start=0
    i_end=0
    while skateDataSet.time[i_start] < new_tricks_interval[0]:
        i_start += 1

    while skateDataSet.time[i_end] < new_tricks_interval[1]:
        i_end += 1

    print("Tricks' start time : " + str(skateDataSet.time[i_start]))
    print("Tricks' end time : " + str(skateDataSet.time[i_end]))

    time_list = skateDataSet.time[i_start:i_end]
    plt.subplot(321)
    df.plotVect(skateDataSet.time, skateDataSet.acceleration, 'Acceleration (m/s2)', 321)
    plt.plot(
        [skateDataSet.time[i_start], skateDataSet.time[i_start], skateDataSet.time[i_end], skateDataSet.time[i_end],
         skateDataSet.time[i_start]], [-abs(max(skateDataSet.normAcceleration[i_start:i_end])),
                                       abs(max(skateDataSet.normAcceleration[i_start:i_end])),
                                       abs(max(skateDataSet.normAcceleration[i_start:i_end])),
                                       -abs(max(skateDataSet.normAcceleration[i_start:i_end])),
                                       -abs(max(skateDataSet.normAcceleration[i_start:i_end]))], color="r")
    plt.subplot(322)
    df.plotVect(skateDataSet.time, skateDataSet.gyroscope, 'Gyroscope (deg/s)', 322)
    plt.plot(
        [skateDataSet.time[i_start], skateDataSet.time[i_start], skateDataSet.time[i_end], skateDataSet.time[i_end],
         skateDataSet.time[i_start]], [-abs(max(skateDataSet.normGyroscope[i_start:i_end])),
                                       abs(max(skateDataSet.normGyroscope[i_start:i_end])),
                                       abs(max(skateDataSet.normGyroscope[i_start:i_end])),
                                       -abs(max(skateDataSet.normGyroscope[i_start:i_end])),
                                       -abs(max(skateDataSet.normGyroscope[i_start:i_end]))], color="r")
    plt.subplot(323)
    df.plotVect(time_list, skateDataSet.acceleration[:,i_start:i_end], 'Acceleration (m/s2)', 323)
    plt.legend(loc='upper right')
    plt.subplot(325)
    plt.plot(time_list, skateDataSet.normAcceleration[i_start:i_end], '-x',label='Norme Accélération', color="black")
    plt.legend(loc='upper right')
    plt.subplot(324)
    df.plotVect(time_list, skateDataSet.gyroscope[:,i_start:i_end], 'Gyroscope (deg/s)', 324)
    plt.legend(loc='upper right')
    plt.subplot(326)
    plt.plot(time_list, skateDataSet.normGyroscope[i_start:i_end], '-x',label="Norme gyroscope", color="black")
    plt.legend(loc='upper right')
    plt.grid()
    plt.tight_layout()
    plt.show()

#---- File extraction ----
"""
    toExtract = str(input("Voulez vous extraire les données d'une figure y/n - other (o):"))

    if toExtract == "y":
        # Tricks to isolate
        tricks_name = str(input("Quelle figure voulez vous extraitre (ollie, kickflip, heelflip, pop_shovit, fs_shovit, 360_flip) :"))
        num_figure = int(input("C'est la combien-ième figure que vous avez enregistré ?"))

        fileTricksPath = "..\\..\\06 - Data\\Isolated_Tricks\\" + tricks_name + "\\" + tricks_name + "_" + str(num_figure) + ".csv"

        df_iso_tricks = skateDataSet.rawData.iloc[i_start:i_end, :]

        dir = os.path.dirname(fileTricksPath)
        if not os.path.exists(dir):
            os.makedirs(dir)
        df_iso_tricks.to_csv(fileTricksPath, sep=",", index=False, index_label=False)

        tricks = sk.SkateboardXXX3000DataSet(fileTricksPath)
        tricks.dispRawData()

    elif toExtract == "o":
        new_mean_time = float(input("Nouveau temps moyen de la figure : "))
        new_tricks_interval[0] = new_mean_time - dt_f
        new_tricks_interval[1] = new_mean_time + dt_f
        i_start = 0
        i_end = 0
        while skateDataSet.time[i_start] < new_tricks_interval[0]:
            i_start += 1
        while skateDataSet.time[i_end] < new_tricks_interval[1]:
            i_end += 1
        df_iso_tricks = skateDataSet.rawData.iloc[i_start:i_end, :]

        plt.plot(df_iso_tricks["time"],df_iso_tricks["normGyr"])
        plt.show()

        toExtract = str(input("Voulez vous extraire les données d'une figure y/n - other (o):"))

        if toExtract == "y":
            tricks_name = str(input(
                "Quelle figure voulez vous extraitre (ollie, kickflip, heelflip, pop_shovit, fs_shovit, 360_flip, pivot) :"))
            num_figure = int(input("C'est la combien-ième figure que vous avez enregistré ?"))

            fileTricksPath = "..\\..\\06 - Data\\Isolated_Tricks\\" + tricks_name + "\\" + tricks_name + "_" + str(
                num_figure) + ".csv"

            df_iso_tricks = skateDataSet.rawData.iloc[i_start:i_end, :]

            dir = os.path.dirname(fileTricksPath)
            if not os.path.exists(dir):
                os.makedirs(dir)
            df_iso_tricks.to_csv(fileTricksPath, sep=",", index=False, index_label=False)

            tricks = sk.SkateboardXXX3000DataSet(fileTricksPath)
"""