import dataSet.SkateboardXXX3000DataSet as sk
import pandas as pd
import tools.SignaleAnalysis as sa
import os
############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

#
completeSequencesPath = "..\\..\\06 - Data\\Raw_sequences\\sesh_151121\\record_3.csv"

#Tricks to isolate
tricks_name = "ollie"

fileTricksPath = "..\\..\\06 - Data\\Isolated_Tricks\\" + tricks_name + "_001.csv"

print("Opening : " + completeSequencesPath)
skateDataSet = sk.SkateboardXXX3000DataSet(completeSequencesPath)
Te = skateDataSet.Te
print("sample frequency : " + str(1 / Te))

skateDataSet.DispRawData()

int_figure = (7.5,9.2) #secondes
index_init = int(int_figure[0] * 1/Te)
index_end = int(int_figure[1]*1/Te)

print(skateDataSet.time[index_init])
print(index_end)
df_iso_tricks = skateDataSet.rawData.iloc[index_init:index_end,:]

dir = os.path.dirname(fileTricksPath)
if not os.path.exists(dir):
    os.makedirs(dir)
df_iso_tricks.to_csv(fileTricksPath, sep=",", index=False, index_label=False)

tricks = sk.SkateboardXXX3000DataSet(fileTricksPath)
tricks.DispRawData()


index_mean = sa.mean_time(tricks.normGyroscope)
print("Index mean : " + str(index_mean))
print("Mean time  : " + str(int_figure[0] + index_mean*Te))