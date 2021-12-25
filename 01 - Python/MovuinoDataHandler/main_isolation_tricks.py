import dataSet.SkateboardXXX3000DataSet as sk
import pandas as pd
import tools.signalAnalysis as sa
import os
import matplotlib.pyplot as plt
############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

completeSequencesPath = "..\\..\\06 - Data\\Raw_sequences\\sesh_181021\\ollie_nb_3.csv"

print("Opening : " + completeSequencesPath)
skateDataSet = sk.SkateboardXXX3000DataSet(completeSequencesPath)
skateDataSet.time =[t/1000 for t in skateDataSet.time]
skateDataSet.rawData["time"] /=1000
Te = skateDataSet.Te/1000
print("sample frequency : " + str(1 / Te))
skateDataSet.DispRawData()

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