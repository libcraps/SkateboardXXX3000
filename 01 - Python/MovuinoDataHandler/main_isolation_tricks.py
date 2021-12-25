import dataSet.SkateboardXXX3000DataSet as sk
import pandas as pd
import tools.signalAnalysis as sa
import tools.DisplayFunctions as df
import os
import matplotlib.pyplot as plt
import numpy as np
############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

completeSequencesPath = "..\\..\\06 - Data\\Raw_sequences\\sesh_181021\\ollie_nb_3.csv"

print("Opening : " + completeSequencesPath)
skateDataSet = sk.SkateboardXXX3000DataSet(completeSequencesPath)
skateDataSet.time =[t/1000 for t in skateDataSet.time]
skateDataSet.rawData["time"] /=1000
Te = skateDataSet.Te/1000
print("sample frequency : " + str(1 / Te))

nb_window = 71
window = [0,nb_window]
overlap = 35

sum_acc = []
sum_gyr = []
time_win = []

normAcc = np.pad(skateDataSet.normAcceleration, (int(nb_window//2), int(nb_window//2)))
normGyr = np.pad(skateDataSet.normGyroscope, (int(nb_window/2), int(nb_window/2)))

while window[1] < len(skateDataSet.time):
    time_win.append(skateDataSet.time[(window[0]+window[1])//2])
    sum_acc.append(np.sum(normAcc[window[0]:window[1]]))
    sum_gyr.append(np.sum(normGyr[window[0]:window[1]]))

    window[0] += nb_window - overlap
    window[1] += nb_window - overlap

print(len(sum_acc))
print(len(skateDataSet.time))
print(len(skateDataSet.time)/len(sum_acc))
#skateDataSet.DispRawData()

time_list = skateDataSet.time
df.PlotVector(time_list, skateDataSet.acceleration, 'Acceleration (m/s2)', 321)
plt.subplot(323)
plt.plot(time_list, skateDataSet.normAcceleration, label='Norme Accélération', color="black")
plt.legend(loc='upper right')
plt.subplot(325)
plt.plot(time_win,sum_acc,'-o', markersize=2)
df.PlotVector(time_list, skateDataSet.gyroscope, 'Gyroscope (deg/s)', 322)
plt.subplot(324)
plt.plot(time_list, skateDataSet.normGyroscope, label="Norme gyroscope", color="black")
plt.legend(loc='upper right')
plt.subplot(326)
plt.plot(time_win,sum_gyr,'-o',markersize=2)

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