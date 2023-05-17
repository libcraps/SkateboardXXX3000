import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

import movuinos.SkateboardXXX3000DataSet as sk
import tools.display_functions as df
import tools.signal_analysis as sa

import models.detection.detection_energy as dt

def insert_row_(row_number, df, row_value):
    df2 = df[row_number:]
    df1 = df[0:row_number]
    if len(df1)>0:
        df1.loc[0] = row_value
    df_result = pd.concat([df1, df2])
    df_result.index = [*range(df_result.shape[0])]
    return df_result


def correction_interpolation(rawData):
    
    n = len(rawData["time"])
    # On s'assure qu'on a 120pt
    interpolateDf = rawData
    if n < 120 and n >0:
        rawData["time"] = np.round(rawData["time"], 2)
        interpolateDf = sk.SkateboardXXX3000DataSet.interpolate_skate_data(rawData, 0.01)

        # interpolateDf.to_csv(f[:-4] + "_interpolated" + ".csv", sep=",", index=False, index_label=False)
        if len(interpolateDf["time"]) > 120:
            interpolateDf = interpolateDf.iloc[0:120, :]

        elif len(interpolateDf["time"]) < 120:
            
            k = 120 - len(interpolateDf["time"])
            print("INTERPOLATION")
            print(k)
            df = interpolateDf.copy()
            for i in range(k):
                if i % 2 == 1:
                    temp = df["time"][0]
                    temp -= 0.01
                    df = insert_row_(0, df, [temp,
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
                                    'gz': df["gz"][0],}, ignore_index=True)
                    df.index = [*range(df.shape[0])]
            interpolateDf = df
    elif n > 120:
        k = (n - 120) // 2
        interpolateDf = rawData.iloc[0:120, :]
    interpolateDf.loc[:,"normAccel"] = np.linalg.norm(np.array([interpolateDf.loc[:,"ax"], interpolateDf.loc[:,"ay"], interpolateDf.loc[:,"az"]]), axis=0)
    interpolateDf.loc[:,"normGyr"] = np.linalg.norm(np.array([interpolateDf.loc[:,"gx"], interpolateDf.loc[:,"gy"], interpolateDf.loc[:,"gz"]]), axis=0)
    return interpolateDf