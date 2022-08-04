"""
Program for the dataprocessing of isolated tricks

"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal

import dataSet.SkateboardXXX3000DataSet as sk
import tools.integratino_functions as ef
import tools.signal_analysis as sa


def Insert_row_(row_number, df, row_value):
    df2 = df[row_number:]
    df1 = df[0:row_number]
    df1.loc[0] = row_value
    df_result = pd.concat([df1, df2])
    df_result.index = [*range(df_result.shape[0])]
    return df_result

############   SETTINGS   #############

device = 'skateboardXXX3000'  # devices available : skateboardXXX3000 / sensitivePen / globalDataSet

folderPath = "..\\..\\06 - Data\\Isolated_Tricks\\"
filename = "record"  # generic name numbers will be added for duplicates

filter = 20

# -------- Data processing ----------------------

listeFichiers = []
liste_len=[]
liste_dt=[]
err=[]

def correctionInterpolation(rawData):
    n = len(rawData["time"])
    # On s'assure qu'on a 120pt
    interpolateDf = rawData
    if n < 120:
        rawData["time"] = np.round(rawData["time"], 2)
        interpolateDf = sk.SkateboardXXX3000DataSet.interpolate_skate_data(rawData, 0.01)

        # interpolateDf.to_csv(f[:-4] + "_interpolated" + ".csv", sep=",", index=False, index_label=False)
        if len(interpolateDf["time"]) > 120:
            interpolateDf = interpolateDf.loc[0:119, :]

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
        interpolateDf = rawData.loc[0:119, :]

    return interpolateDf


for (repertoire, sousRepertoires, fichiers) in os.walk(folderPath):
    if "OLD" not in repertoire:
        for file in fichiers:
            print(repertoire)
            f = os.path.join(repertoire, file)
            trickDataSet = sk.SkateboardXXX3000DataSet(f)
            Te = trickDataSet.Te

            newDF = correctionInterpolation(trickDataSet.rawData)
            newDF = sk.SkateboardXXX3000DataSet.normalized_L2(newDF)
            try :
                del newDF['ax_normalized_1']
                del newDF['ay_normalized_1']
                del newDF['az_normalized_1']
                del newDF['gx_normalized_1']
                del newDF['gy_normalized_1']
                del newDF['gz_normalized_1']
                newDF.to_csv(f, sep=",", index=False, index_label=False)
            except (RuntimeError, TypeError, NameError,KeyError):
                pass
            newDF.to_csv(f, sep=",", index=False, index_label=False)