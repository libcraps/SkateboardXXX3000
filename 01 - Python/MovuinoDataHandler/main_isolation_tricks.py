import dataSet.SkateboardXXX3000DataSet as sk
import pandas as pd
import tools.signalAnalysis as sa
import tools.DisplayFunctions as df
import os
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import find_peaks
############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

completeSequencesPath = "..\\..\\06 - Data\\Raw_sequences\\sesh_181021\\record_8.csv"

print("Opening : " + completeSequencesPath)
skateDataSet = sk.SkateboardXXX3000DataSet(completeSequencesPath)
skateDataSet.time =[t/1000 for t in skateDataSet.time]
skateDataSet.rawData["time"] /=1000
Te = skateDataSet.Te/1000
print("sample period : " + str(Te))
print("sample frequency : " + str(1 / Te))


#------- PEAK DETECTION ----------
nb_window = int(1/Te*0.5)

if nb_window%2 == 0 :
    nb_window+=1

window = [0,nb_window]
overlap = int(nb_window//2)

retard = nb_window//2

sum_acc = []
sum_gyr = []
time_win = []

list_dt = [skateDataSet.time[i]-skateDataSet.time[i-1] for i in range(1,skateDataSet.nb_row)]
list_dt=np.pad(list_dt, (1,0))

plt.plot(skateDataSet.time,list_dt)
plt.show()
normAcc = np.pad(skateDataSet.normAcceleration, (int(nb_window//2), int(nb_window//2)))
normGyr = np.pad(skateDataSet.normGyroscope, (int(nb_window/2), int(nb_window/2)))

while window[1] < len(skateDataSet.time):
    time_win.append(skateDataSet.time[(window[0]+window[1])//2 - retard])
    sum_acc.append(np.mean(normAcc[window[0]:window[1]]))
    sum_gyr.append(np.mean(normGyr[window[0]:window[1]]))

    window[0] += nb_window - overlap
    window[1] += nb_window - overlap

sum_gyr=np.array(sum_gyr)
peaks_gyr, _ = find_peaks(sum_gyr, prominence=10)
time_win = np.array(time_win)

dt_i = 0.8
dt_f = 0.6

tricks_interval = []
for i in peaks_gyr:
    if time_win[i]-dt_i < 0 :
        tricks_interval.append([0.1, time_win[i] + dt_i])
    else:
        tricks_interval.append([time_win[i]-dt_i, time_win[i]+dt_i])
print(tricks_interval)
#skateDataSet.DispRawData()
time_list = np.array(skateDataSet.time)
df.PlotVector(time_list, skateDataSet.acceleration, 'Acceleration (m/s2)', 321)
plt.plot(time_win,sum_acc,'-o', markersize=2, color="grey")
plt.legend(loc='upper right')
plt.subplot(323)
plt.plot(time_list, skateDataSet.normAcceleration, label='Norme Accélération', color="black")
plt.legend(loc='upper right')
plt.subplot(325)
plt.plot(time_win,sum_acc,'-o', markersize=2)
df.PlotVector(time_list, skateDataSet.gyroscope, 'Gyroscope (deg/s)', 322)
plt.plot(time_win, sum_gyr,'-o', markersize=2, color="grey")
plt.plot(time_win[peaks_gyr], sum_gyr[peaks_gyr], "v", markersize=5, color="orange", label="Peaks")
plt.legend(loc='upper right')
plt.subplot(324)
plt.plot(time_list, skateDataSet.normGyroscope, label="Norme gyroscope", color="black")
plt.legend(loc='upper right')
plt.subplot(326)
plt.plot(time_win, sum_gyr,'-o', markersize=2)
plt.grid()
plt.show()

#------------ PEAKS ISOLATION ------------------

for k in range(len(tricks_interval)):
    i_start = int(float(tricks_interval[k][0]-0.1)/Te)
    i_end = int(float(tricks_interval[k][1]-0.1)/Te)
    print(i_start)
    while skateDataSet.time[i_start] < tricks_interval[k][0]:
        i_start += 1

    while skateDataSet.time[i_end] < tricks_interval[k][1]:
        i_end += 1

    print("Tricks' start time : " + str(skateDataSet.time[i_start]))
    print("Tricks' end time : " + str(skateDataSet.time[i_end]))

    df_iso_tricks = skateDataSet.rawData.iloc[i_start:i_end,:]

    normGyroscope = list(df_iso_tricks["normGyr"])
    time = list(df_iso_tricks["time"])

    # ---- Temps moyen de la norme du gyrosocpe ------
    index_mean_loc = sa.mean_time(normGyroscope)
    print("Index mean : " + str(index_mean_loc))
    print("Mean time  : " + str(skateDataSet.time[i_start] + index_mean_loc*Te))

    mean_time = skateDataSet.time[i_start] + index_mean_loc*Te
    index_mean_glob = 0

    new_tricks_interval = (mean_time-dt_f, mean_time+dt_f)
    i_start=0
    i_end=0
    while skateDataSet.time[i_start] < new_tricks_interval[0]:
        i_start += 1

    while skateDataSet.time[i_end] < new_tricks_interval[1]:
        i_end += 1

    print("Tricks' start time : " + str(skateDataSet.time[i_start]))
    print("Tricks' end time : " + str(skateDataSet.time[i_end]))
    df_iso_tricks = skateDataSet.rawData.iloc[i_start:i_end,:]

    time_list = skateDataSet.time[i_start:i_end]
    plt.subplot(321)
    df.PlotVector(skateDataSet.time, skateDataSet.acceleration, 'Acceleration (m/s2)', 321)
    plt.plot(
        [skateDataSet.time[i_start], skateDataSet.time[i_start], skateDataSet.time[i_end], skateDataSet.time[i_end],
         skateDataSet.time[i_start]], [-abs(max(skateDataSet.normAcceleration[i_start:i_end])),
                                       abs(max(skateDataSet.normAcceleration[i_start:i_end])),
                                       abs(max(skateDataSet.normAcceleration[i_start:i_end])),
                                       -abs(max(skateDataSet.normAcceleration[i_start:i_end])),
                                       -abs(max(skateDataSet.normAcceleration[i_start:i_end]))], color="r")
    plt.subplot(322)
    df.PlotVector(skateDataSet.time, skateDataSet.gyroscope, 'Acceleration (m/s2)', 322)
    plt.plot(
        [skateDataSet.time[i_start], skateDataSet.time[i_start], skateDataSet.time[i_end], skateDataSet.time[i_end],
         skateDataSet.time[i_start]], [-abs(max(skateDataSet.normGyroscope[i_start:i_end])),
                                       abs(max(skateDataSet.normGyroscope[i_start:i_end])),
                                       abs(max(skateDataSet.normGyroscope[i_start:i_end])),
                                       -abs(max(skateDataSet.normGyroscope[i_start:i_end])),
                                       -abs(max(skateDataSet.normGyroscope[i_start:i_end]))], color="r")
    plt.subplot(323)
    df.PlotVector(time_list, skateDataSet.acceleration[i_start:i_end], 'Acceleration (m/s2)', 323)
    plt.legend(loc='upper right')
    plt.subplot(325)
    plt.plot(time_list, skateDataSet.normAcceleration[i_start:i_end], '-x',label='Norme Accélération', color="black")
    plt.legend(loc='upper right')
    plt.subplot(324)
    df.PlotVector(time_list, skateDataSet.gyroscope[i_start:i_end], 'Gyroscope (deg/s)', 324)
    plt.legend(loc='upper right')
    plt.subplot(326)
    plt.plot(time_list, skateDataSet.normGyroscope[i_start:i_end], '-x',label="Norme gyroscope", color="black")
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()




"""
toExtract = str(input("Vous les vous extraire les données d'une figure y/n :"))

if toExtract == "y":
    #Tricks to isolate
    tricks_name = "ollie" # choose btw : ollie, kickflip, heelflip, pop_shovit, fs_shovit, 360_flip
    tricks_interval = (23.5, 24.5) #secondes

    #tricks_name = str(input("Quelle figure voulez vous extraitre (ollie, kickflip, heelflip, pop_shovit, fs_shovit, 360_flip) :"))
    #str_interval = input("Dans quel interval de temps se situe la figure ?")
    #tricks_interval = tuple(float(x) for x in str_interval.split(","))
    num_figure = int(input("C'est la combien-ième figure que vous avez enregistré ?"))

    fileTricksPath = "..\\..\\06 - Data\\Isolated_Tricks\\" + tricks_name + "\\" + tricks_name + "_" + str(num_figure)+".csv"

    dt = 0.6

    index_init = int((float(tricks_interval[0])-1)*1/Te)
    index_end = int((float(tricks_interval[1])-1)*1/Te)

    while skateDataSet.time[index_init] < tricks_interval[0]:
        index_init += 1

    while skateDataSet.time[index_end] < tricks_interval[1]:
        index_end += 1

    print("Tricks' start time : " + str(skateDataSet.time[index_init]))
    print("Tricks' end time : " + str(skateDataSet.time[index_end]))

    df_iso_tricks = skateDataSet.rawData.iloc[index_init:index_end,:]

    normGyroscope = list(df_iso_tricks["normGyr"])
    time = list(df_iso_tricks["time"])

    plt.plot(time,normGyroscope)
    plt.show()

    # ---- Temps moyen de la norme du gyrosocpe ------
    index_mean_loc = sa.mean_time(normGyroscope)
    print("Index mean : " + str(index_mean_loc))
    print("Mean time  : " + str(skateDataSet.time[index_init] + index_mean_loc*Te))

    mean_time = skateDataSet.time[index_init] + index_mean_loc*Te
    index_mean_glob = 0

    new_tricks_interval = (mean_time-dt, mean_time+dt)
    index_init=0
    index_end=0
    while skateDataSet.time[index_init] < new_tricks_interval[0]:
        index_init += 1

    while skateDataSet.time[index_end] < new_tricks_interval[1]:
        index_end += 1

    print(new_tricks_interval)
    print("Tricks' start time : " + str(skateDataSet.time[index_init]))
    print("Tricks' end time : " + str(skateDataSet.time[index_end]))
    df_iso_tricks = skateDataSet.rawData.iloc[index_init:index_end,:]

    dir = os.path.dirname(fileTricksPath)
    if not os.path.exists(dir):
        os.makedirs(dir)
    df_iso_tricks.to_csv(fileTricksPath, sep=",", index=False, index_label=False)

    tricks = sk.SkateboardXXX3000DataSet(fileTricksPath)
    tricks.DispRawData()
"""