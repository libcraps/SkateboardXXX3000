
import numpy as np
import pandas as pd
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import find_peaks


def meanTime(dat):
    """
    Return the mean index of the incoming data
    :param dat:
    :return:
    """
    i_mean = 0
    E_t = 0
    E = 0
    for i in range(len(dat)):
        E_t += i*dat[i]**2
        E += dat[i]**2

    i_mean = int(E_t/E)
    return i_mean



def areaUnderCurve(x,y):
    """
    Calculate the area under a curve of a signal y given its timeLine x

    :param x:
    :param y:
    :return:
    """
    area = 0
    for k in range(len(x) - 1):
        dt = x[k + 1] - x[k]
        area += (y[k + 1] + y[k]) * dt / 2

    return area

def eventDetection(skateDataSet,size_window,overlap, prominence, distance):
    if size_window % 2 == 0:
        size_window += 1

    window = [0, size_window]
    retard = size_window // 2

    sum_acc = []
    sum_gyr = []

    time_win = []

    output = []

    normAcc = np.pad(skateDataSet.normAcceleration, (int(size_window // 2), int(size_window // 2)))
    normGyr = np.pad(skateDataSet.normGyroscope, (int(size_window // 2), int(size_window // 2)))

    while window[1] < len(skateDataSet.time):
        time_win.append(skateDataSet.time[(window[0] + window[1]) // 2 - retard])
        sum_acc.append(np.mean(normAcc[window[0]:window[1]]))
        sum_gyr.append(np.mean(normGyr[window[0]:window[1]]))

        window[0] += size_window - overlap
        window[1] += size_window - overlap

    sum_gyr = np.array(sum_gyr)
    sum_acc = np.array(sum_acc)
    peaks_gyr, _gyr = find_peaks(sum_gyr, prominence=prominence, distance=distance)
    peaks_acc, _acc = find_peaks(sum_acc, prominence=prominence - 1, distance=distance - 2)
    time_win = np.array(time_win)

    peaks_tricks = []
    delta_peak = 2

    for i, peak_a in enumerate(peaks_acc):
        for j, peak_g in enumerate(peaks_gyr):
            if peak_g - delta_peak < peak_a < peak_g + delta_peak:
                peaks_tricks.append(peak_g)

    dt_i = 0.8


    tricks_interval = []
    for i in peaks_tricks:
        if time_win[i] - dt_i < 0:
            tricks_interval.append([0.1, time_win[i] + dt_i])
        else:
            tricks_interval.append([time_win[i] - dt_i, time_win[i] + dt_i])

    return time_win, tricks_interval, peaks_gyr, peak_a, peaks_tricks

def centerEvents(skateDataSet,tricks_interval, dt_f = 0.6):
    time_list = []
    Te = skateDataSet.Te
    for k in range(len(tricks_interval)):
        # We're looking for the best index that matches with the time interval
        i_start = int(float(tricks_interval[k][0] - 0.1) / Te)
        i_end = int(float(tricks_interval[k][1] - 0.1) / Te)

        while skateDataSet.time[i_start] < tricks_interval[k][0]:
            i_start += 1

        while skateDataSet.time[i_end] < tricks_interval[k][1]:
            i_end += 1

        df_iso_tricks = skateDataSet.interpolateData.iloc[i_start:i_end, :]

        normGyroscope = list(df_iso_tricks["normGyr"])
        time = list(df_iso_tricks["time"])

        # ---- Temps moyen de la norme du gyrosocpe ------
        index_mean_loc = meanTime(normGyroscope)

        # teeest :
        # g = np.cumsum(skateDataSet.normGyroscope[i_start:i_end])
        # index_mean_loc = np.argmin(np.abs(g - np.amax(g) / 2))
        mean_time = skateDataSet.time[i_start] + index_mean_loc * Te

        new_tricks_interval = [mean_time - dt_f, mean_time + dt_f]
        i_start = 0
        i_end = 0
        while skateDataSet.time[i_start] < new_tricks_interval[0]:
            i_start += 1

        while skateDataSet.time[i_end] < new_tricks_interval[1]:
            i_end += 1

        time_list.append([i_start,i_end])
    return time_list

def mean_moving_window(data, size_window, overlap):
    if size_window%2 == 0 :
        size_window+=1

    window = [0, size_window]
    retard = size_window // 2
    output=[]
    time_win = []

    output = []

    dat = np.pad(data, (int(size_window // 2), int(size_window // 2)))

    while window[1] < len(data):
        output.append(np.mean(dat[window[0]:window[1]]))

        window[0] += size_window - overlap
        window[1] += size_window - overlap

    return np.array(output)

def correlate_tricks(dataSet1, dataSet2):
    cor = [0]*6
    cor_gx = signal.correlate(dataSet1["gx_normalized_1"], dataSet2["gx_normalized_1"])
    cor_gy = signal.correlate(dataSet1["gy_normalized_1"], dataSet2["gy_normalized_1"])
    cor_gz = signal.correlate(dataSet1["gz_normalized_1"], dataSet2["gz_normalized_1"])
    cor_ay = signal.correlate(dataSet1["ay_normalized_1"], dataSet2["ay_normalized_1"])
    cor_ax = signal.correlate(dataSet1["ax_normalized_1"], dataSet2["ax_normalized_1"])
    cor_az = signal.correlate(dataSet1["az_normalized_1"], dataSet2["az_normalized_1"])

    cor[0] = max(cor_ax)
    cor[1] = max(cor_ay)
    cor[2] = max(cor_az)
    cor[3] = max(cor_gx)
    cor[4] = max(cor_gy)
    cor[5] = max(cor_gz)

    return cor